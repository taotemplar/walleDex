from substrateinterface import Keypair
import multiprocessing
import time
import argparse

import collections


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
    if args.skip_5 is True:
        starting_positions = [1,2]

    attempt = 0
    while True:
        keypair = Keypair.create_from_mnemonic(Keypair.generate_mnemonic())
        address = keypair.ss58_address
        address_lower = address.lower()

        for offset in starting_positions:
            matched_prefix = trie.search(address_lower[offset:])
            if matched_prefix:
                queue.put((keypair, attempt + 1, matched_prefix))
                attempt = 0

        attempt += 1

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
        elif len(word) > 10: continue

        for letter in word:
            if letter not in 'abcdefghijklmnopqrstuvwxyz0123456789':
                print(f'Cannot use {w}, because it has a non-alpha-numeric character: {letter}')
                continue

        chosen_words.append(word)
        if len(word) > 4: #Only use alternate letters to make longer words
            for index, letter in enumerate(word):

                for letter_key, letter_val in alternate_letters:
                    if letter == letter_key:
                        alternate_spelling_word = word[:index] + letter_val + word[index+1:]
                        chosen_words.append(alternate_spelling_word)
    return chosen_words

def parseArgs():

    parser = argparse.ArgumentParser(description='Creates vast numbers of vanity wallets quickly')

    # Add an argument for the number of letters
    parser.add_argument('-n', '--min-num-letters', type=int, default=4, help='Min word length from words.txt file')
    parser.add_argument('-s', '--skip-5', action='store_true', help='Skip using the 5 as an "s" at the start of a word')

    # Parse the arguments
    return parser.parse_args()

    # Validate the number of letters
    return args

def generate_vanity_wallet_parallel(prefixes, processes, result_queue, args):
    """
    Generate a Bittensor vanity wallet using multiple processes.
    """
    start_time = time.time()

    total_attempts = 0
    while True:
        # Wait for one process to find a match or all to complete
        for p in processes:
            if not p.is_alive():
                raise Exception("Process died, this shouldn't happen...")
        while result_queue.empty() and any(p.is_alive() for p in processes):
            time.sleep(0.1)  # Avoid busy-waiting

        # If a result is found, terminate all processes
        if not result_queue.empty():
            keypair, attempts, match_word = result_queue.get()
            total_attempts += attempts
#            for p in processes:
#                p.terminate()

            elapsed_time = time.time() - start_time
            with open('results.txt','a') as f:
                f.write(f"\n{match_word} Found a match after ~{attempts} addresses in {elapsed_time:.2f} seconds! [{attempts/elapsed_time:.1f} addresses/second]\n")
                f.write(f"{match_word} -> {keypair.ss58_address}\n")
                f.write(f"Mnemonic: {keypair.mnemonic}\n")
                f.write(f"Public Key: {keypair.public_key.hex()}\n")
                f.write(f"Private Key: {keypair.private_key.hex()}\n")
            print(f'{match_word}: {keypair.ss58_address}')
            return keypair

if __name__ == "__main__":
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
        vanity_keypair = generate_vanity_wallet_parallel(chosen_words, processes, result_queue, args)
