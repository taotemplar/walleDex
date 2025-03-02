from substrateinterface import Keypair
import multiprocessing
import time
import argparse
from rich.console import Console

import collections


class NotAliveException(Exception): pass

class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, address):
        node = self.root
        prefix = ""
        for char in address:
            if char not in node.children:
                return None
            node = node.children[char]
            prefix += char
            if node.is_end_of_word:
                return prefix
        return None


def search_for_vanity(prefixes, queue, args):
    trie = Trie()
    for prefix in prefixes:
        trie.insert(prefix)

    starting_positions = [0,1,2]
    if not args.use_5_as_S:
        starting_positions = [1,2]

    attempt = 0
    while True:
        try:
            keypair = Keypair.create_from_mnemonic(Keypair.generate_mnemonic())
            address = keypair.ss58_address
            address_lower = address.lower()

            for offset in starting_positions:
                matched_prefix = trie.search(address_lower[offset:])
                if matched_prefix:
                    if not args.pretty or isPretty(address, matched_prefix, offset):
                        queue.put((keypair, attempt + 1, matched_prefix))
                        attempt = 0

            attempt += 1
        except KeyboardInterrupt:
            return

def pickWords(args):
    # Get the word list
    with open('words.txt','r') as f:
        lines = f.read()
        word_list = lines.split('\n')


    chosen_words = []
    alternate_letters = [('s','5'), ('i','1'), ('e','3'), ('o','0')]
    for w in word_list:
        word = w.lower()

        if len(word) < args.min_num_letters: continue

        for letter in word:
            if letter not in 'abcdefghijklmnopqrstuvwxyz0123456789':
                print(f'Cannot use {w}, because it has a non-alpha-numeric character: {letter}')
                continue

        chosen_words.append(word)
        if not args.no_alternate_letters:
            for index, letter in enumerate(word):

                for letter_key, letter_val in alternate_letters:
                    if letter == letter_key:
                        alternate_spelling_word = word[:index] + letter_val + word[index+1:]
                        chosen_words.append(alternate_spelling_word)

    return chosen_words

def generate_vanity_wallet_parallel(prefixes, processes, result_queue, args):
    """
    Generate a Bittensor vanity wallet using multiple processes.
    """
    start_time = time.time()

    while True:

        for p in processes:
            if not p.is_alive():
                raise NotAliveException()
        while result_queue.empty() and any(p.is_alive() for p in processes):
            time.sleep(0.1)  # Avoid busy-waiting

        if not result_queue.empty():
            keypair, attempts, match_word = result_queue.get()

            elapsed_time = time.time() - start_time
            with open('rawAddresses.txt','a') as f:
                f.write(f"\n[{match_word}:{keypair.ss58_address}] Found a match after ~{attempts} address checks.\n")
                f.write(f"Mnemonic: {keypair.mnemonic}\n")
                f.write(f"Public Key: {keypair.public_key.hex()}\n")
                f.write(f"Private Key: {keypair.private_key.hex()}\n")
            printAddress(console, match_word, keypair.ss58_address)
            return keypair

console = Console()
def printAddress(console, rawAddressWord, address):
    wordStartIndex = address.lower().find(rawAddressWord.lower())
    before = address[:wordStartIndex]
    highlightedWord = address[wordStartIndex:wordStartIndex+len(rawAddressWord)]
    after = address[wordStartIndex+len(rawAddressWord):]
    console.print(f'{before}[red]{highlightedWord}[/red]{after}')


def isPretty(address, word, offset):
    addressStartIndex = 0
    addy_lower = address.lower()
    word_lower = word.lower()
    for index, addyLetter in enumerate(address):
        if addy_lower[index:].startswith(word_lower):
            addressStartIndex = index
            break

    addressStartIndex = offset
    wordInAddress = address[addressStartIndex:len(word)+addressStartIndex]

    #Ignore words with numbers
    if any(char.isdigit() for char in wordInAddress):
        return False
    #Pick words that start with a capital
    if wordInAddress[0].isupper() and wordInAddress[1:].islower():
        return True
    #Pick words that are uppercase or lowercase
    if wordInAddress.isupper() or wordInAddress.islower():
        return True
    #Throw out the rest
    return False


def parseArgs():

    parser = argparse.ArgumentParser(description='Creates vast numbers of vanity wallets quickly')

    parser.add_argument('-n', '--min-num-letters', type=int, default=4, help='Min word length from words.txt file')
    parser.add_argument('-s', '--use-5-as-S', action='store_true', help='Use the 5 as an "s" at the start of a word')
    parser.add_argument('--no-alternate-letters', action='store_true', help='Do not find words by replacing letters with numbers (for example, dont match: 3l1te, 5hark, d0rk)')
    parser.add_argument('-p', '--pretty', action='store_true', help='Only find words that start with a capital, or all uppercase, or all lowercase.  DOES NOT MATCH ANY WORDS WITH NUMBERS!')

    return parser.parse_args()


def main():
    args = parseArgs()
    chosen_words = pickWords(args)
    print(f"Starting to search for '{len(chosen_words)}' prefixes...")
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    result_queue = multiprocessing.Queue() # Create a queue to collect results from processes

    # Create a pool of processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(
            target=search_for_vanity,
            args=(chosen_words, result_queue, args)
        )
        p.start()
        processes.append(p)


    while True:
        try:
            vanity_keypair = generate_vanity_wallet_parallel(chosen_words, processes, result_queue, args)
        except (KeyboardInterrupt, NotAliveException):
            print('Ending')
            return

if __name__ == "__main__":
    main()
