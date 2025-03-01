# bittensorVanityWalletGenerator
Generate vast amounts of vanity wallets quickly to pick from

# Step 0. Installation
Clone this repo
`git clone stuff`

Install virtualenv
`pip3 install virtualenv`
`virtualenv ~/.venvs/vanityDex`

Activate virtual env
`source ~/.venvs/vanityDex/bin/activate`
`cd the cloned repo`
`pip -r requirements.txt`



# Step 1. Run the generator

`python3 generateWallets.py`

Wallets are printed to console and their key/mnemonics are stored in results.txt

![image](https://github.com/user-attachments/assets/c5a22bcb-2498-4641-8e0e-c9b37970490f)

Tip: `python3 generateWallets.py --help` for parameters to change what wallets are saved.


# Step 2. View the generated mnemonics

Open `results.txt` with your favorite/safest editor to view the mnemonics that create the wallets you've generated.  Ideally one that does not keep history (like notepad or something)

# Step 3. View your vanityDex

`python3 vanityDex.py`

![image](https://github.com/user-attachments/assets/367772eb-c810-418e-b9a7-318efcced054)

Set a goal, try to catch all the words of a particular length, and attempt to get pretties.

Tip: `python3 vanityDex.py --help` to view wallets and filtering options

# Step 4. The game

Just like in pokemon, not everyone's path or goals are the same.  You can carve your own goals.

Here are some ideas:

* Do you want to catch them all?  Try filling out the 3 letter words, then work on the 4 letter words, etc.
  * `python3 generateWallets.py -n=4` `-n=` parameter is your friend here, increasing as needed
* Do you only want to catch long worded wallets?
  * `python3 generateWallets.py -n=6` `-n=` parameter is helpful here again, probably with a minimum of 5.
* Do you only want to catch pretty worded wallets?
  * `python3 generateWallets.py -p` `-p` parameter only looks for words that are --pretty.  Eg: ALLUPPERCASE or alllowercase or Startwithacapital.
* What about legendary wallets?
  * Legendary wallets are those that have more than 1 word, the word may be after the first word in the address OR at the end of the wallet address.
  * Eg: 5FIRExlkc...3udSALT
  * `python3 vanityDex.py -l` for spotting your legendaries.
* Are you a pokemaniac?
  * `python3 vanityDex.py -poke` for spotting your pokemon.

# Step 5. Results.txt size
* But be wary of your `results.txt` size.  It can grow fast if you don't use parameters with `python3 generateWallets.py` !

# Step 6. Actually using the wallet
* Never copy a mnemonic from `results.txt` to your clipboard, never save it outside of the file.
* Physically write the mnemonic of the wallet you want to use to a piece of paper outside of your computer.  Then write it down again (2 pieces of paper).  See 44:44 here in this video for a run-down of how to safely store a mnemonic https://www.youtube.com/watch?v=UH_sOZSIk10&t=796s .
* DELETE the wallet's mnemonic from the `results.txt` file.  Save and close the file.
* Then manually type in the mnemonic to your favorite wallet app by looking at your paper mnemonic.

Happy vanity wallet hunting!
