
import argparse
import subprocess
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

POKEMON = [
'bulbasaur',
'ivysaur',
'venusaur',
'charmander',
'charmeleon',
'charizard',
'squirtle',
'wartortle',
'blastoise',
'caterpie',
'metapod',
'butterfree',
'weedle',
'kakuna',
'beedrill',
'pidgey',
'pidgeotto',
'pidgeot',
'rattata',
'raticate',
'spearow',
'fearow',
'ekans',
'arbok',
'pikachu',
'raichu',
'sandshrew',
'sandslash',
'nidoran',
'nidorina',
'nidoqueen',
'nidoran',
'nidorino',
'nidoking',
'clefairy',
'clefable',
'vulpix',
'ninetales',
'jigglypuff',
'wigglytuff',
'zubat',
'golbat',
'oddish',
'gloom',
'vileplume',
'paras',
'parasect',
'venonat',
'venomoth',
'diglett',
'dugtrio',
'meowth',
'persian',
'psyduck',
'golduck',
'mankey',
'primeape',
'growlithe',
'arcanine',
'poliwag',
'poliwhirl',
'poliwrath',
'abra',
'kadabra',
'alakazam',
'machop',
'machoke',
'machamp',
'bellsprout',
'weepinbell',
'victreebel',
'tentacool',
'tentacruel',
'geodude',
'graveler',
'golem',
'ponyta',
'rapidash',
'slowpoke',
'slowbro',
'magnemite',
'magneton',
'farfetchd',
'doduo',
'dodrio',
'seel',
'dewgong',
'grimer',
'muk',
'shellder',
'cloyster',
'gastly',
'haunter',
'gengar',
'onix',
'drowzee',
'hypno',
'krabby',
'kingler',
'voltorb',
'electrode',
'exeggcute',
'exeggutor',
'cubone',
'marowak',
'hitmonlee',
'hitmonchan',
'lickitung',
'koffing',
'weezing',
'rhyhorn',
'rhydon',
'chansey',
'tangela',
'kangaskhan',
'horsea',
'seadra',
'goldeen',
'seaking',
'staryu',
'starmie',
'mrMime',
'scyther',
'jynx',
'electabuzz',
'magmar',
'pinsir',
'tauros',
'magikarp',
'gyarados',
'lapras',
'ditto',
'eevee',
'vaporeon',
'jolteon',
'flareon',
'porygon',
'omanyte',
'omastar',
'kabuto',
'kabutops',
'aerodactyl',
'snorlax',
'articuno',
'zapdos',
'moltres',
'dratini',
'dragonair',
'dragonite',
'mewtwo',
'mew',
]

def grepFile(filename, pattern):
    try:
        # Run grep command and capture output
        result = subprocess.run(
            ['grep', pattern, filename],
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()  # Return list of matching lines
    except FileNotFoundError:
        return "File not found"
    except subprocess.CalledProcessError:
        return "No matches found"


def generateDex():
    with open('words.txt','r') as f:
        lines = f.read()
        word_list = lines.split('\n')
    baseDex = {}
    for word in word_list:
        if word == '': continue
        baseDex[word.lower()] = []
    return baseDex


def extractWord(text):
    return re.findall(r'\[(.+):(.+)\]', text)[0]


def peerAtCaughtWords():
    caughtWords = grepFile('rawAddresses.txt', r'\[.*\]')
    return [extractWord(line) for line in caughtWords]


def populateDex(caughtWords):
    vanityDex = generateDex()
    for word, address in caughtWords:
        if word.lower() in vanityDex:
            wordStartIndex = address.lower().find(word.lower())
            wordInAddress = address[wordStartIndex:wordStartIndex+len(word)]
            vanityDex[word.lower()].append((wordInAddress, address))
    return vanityDex


def printDex(vanityDex, caughtWords, args):
    console = Console()
    maxWordLength = max([len(word) for word in vanityDex]) + 1
    totalsDict = {'totals':{},
                  'baseCaught':{},
                  'prettyCount':{},
                  'pokemon':{},
                  'prettyPokemonCaught':{},
                  }


    wordSet = set([word for word in vanityDex])
    wordsTuple = tuple(wordSet)

    #Start counting at 0
    for i in range(maxWordLength):
        for totals in totalsDict:
            totalsDict[totals][i] = 0


    for word_key in vanityDex:
        totalsDict['totals'][len(word_key)] += 1
        if len(vanityDex[word_key]) > 0:
            totalsDict['baseCaught'][len(word_key)] += 1
            if word_key.lower() in POKEMON:
                totalsDict['pokemon'][len(word_key)] += 1

            for rawAddressWord, address in vanityDex[word_key]:
                if isPretty(rawAddressWord):
                    totalsDict['prettyCount'][len(word_key)] += 1
                    if word_key.lower() in POKEMON:
                        totalsDict['prettyPokemonCaught'][len(word_key)] += 1
                    break


    if args.show_pokemon:
        for word_key in vanityDex:
            if word_key.lower() in POKEMON:
                if len(vanityDex[word_key]) > 0:
                    for rawAddressWord, address in vanityDex[word_key]:
                        if (not args.show_pretty or isPretty(rawAddressWord)) \
                         and (not args.legendary or isLegendary(rawAddressWord, address, wordsTuple)):
                            printAddress(console, rawAddressWord, address)


    if not args.show_pokemon and (args.find or args.min_characters or args.legendary):
        for word_key in vanityDex:
            if len(vanityDex[word_key]) == 0: continue
            if not args.find or word_key.startswith(args.find.lower()):
                if len(word_key) >= (args.min_characters or 3):
                    for rawAddressWord, address in vanityDex[word_key]:
                        if (not args.show_pretty or isPretty(rawAddressWord)) \
                         and (not args.legendary or isLegendary(rawAddressWord, address, wordsTuple)):
                            printAddress(console, rawAddressWord, address)


    print('')


    table = Table(title="Vanity Dex", header_style="bold white on dark_blue", box=box.SIMPLE_HEAVY)
    table.add_column("Letter Count", justify="right", style="bright_cyan")
    table.add_column("Caught", justify="right", style="white")
    table.add_column("Pretties Caught", justify="right", style="yellow")
    table.add_column("Pokemon Caught", justify="right", style="white")
    table.add_column("Pretty Pokemon Caught", justify="right", style="cyan1")

    for length in range(15):
        if length < 3: continue

        table.add_row(
            str(length),
            f"{totalsDict['baseCaught'][length]}/{totalsDict['totals'][length]}",
            f"{totalsDict['prettyCount'][length]}/{totalsDict['totals'][length]}",
            f"{totalsDict['pokemon'][length]}/{len([p for p in POKEMON if len(p) == length])}",
            f"{totalsDict['prettyPokemonCaught'][length]}/{len([p for p in POKEMON if len(p) == length])}",
        )

    table.add_section()
    table.add_row(
        'Totals',
        f"{sum([1 for word in vanityDex if vanityDex[word] and len(word) >= 3])}",
        f"{sum([totalsDict['prettyCount'][number] for number in totalsDict['prettyCount'] if number >= 3])}",
        f"{sum([totalsDict['pokemon'][length] for length in totalsDict['pokemon']])}",
        f"{sum([totalsDict['prettyPokemonCaught'][length] for length in totalsDict['prettyPokemonCaught']])}",
    )


    console.print(table)

def printAddress(console, rawAddressWord, address):
    wordStartIndex = address.find(rawAddressWord)
    before = address[:wordStartIndex]
    highlightedWord = address[wordStartIndex:wordStartIndex+len(rawAddressWord)]
    after = address[wordStartIndex+len(rawAddressWord):]
    console.print(f'{before}[red]{highlightedWord}[/red]{after}')


def parseArgs():
    parser = argparse.ArgumentParser(description='Displays your vanity wallet dex')

    parser.add_argument('-poke', '--show-pokemon', action='store_true', help='Filter to only pokemon wallets you own')
    parser.add_argument('-p', '--show-pretty', action='store_true', help='Filter to only pretty wallets')
    parser.add_argument('-n', '--min-characters', type=int, help='Filter by minimum number of characters')
    parser.add_argument('-l', '--legendary', action='store_true', help='Filter to only wallets that start with words and end with words.')
    parser.add_argument(
        '-f',
        '--find',
        type=str,
        required=False,
        help='Search for words that start with this string (eg: "se" returns search, second, setup, etc)'
    )

    return parser.parse_args()

def isLegendary(rawAddressWord, address, wordsTuple):
    wordStartIndex = address.find(rawAddressWord)
    if wordStartIndex > len(address) / 2:
        #If word occurs in second half of the address, we never found a word at the front, so its not legendary
        return False
    addressAfterFirstWord = address[wordStartIndex+len(rawAddressWord):]
    return any(address.endswith(word) for word in wordsTuple) or any(addressAfterFirstWord.startswith(word) for word in wordsTuple)

def isPretty(word):
    return isTitleCase(word) or word.islower() or word.isupper()

def isTitleCase(word):
    return word != '' and word[0].isupper() and word[1:].islower()

if __name__ == "__main__":
    args = parseArgs()
    if args.legendary:
        print('Finding legendaries can be slow if you have many wallets...')
    caughtWords = peerAtCaughtWords()
    vanityDex = populateDex(caughtWords)
    printDex(vanityDex, caughtWords, args)
