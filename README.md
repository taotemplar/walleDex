# bittensorVanityWalletGenerator
Generate vast amounts of vanity wallets quickly to pick from

# Step 1. Run the generator

`python3 generateWallets.py`

Wallets are printed to console and their key/mnemonics are stored in results.txt

![image](https://github.com/user-attachments/assets/c5a22bcb-2498-4641-8e0e-c9b37970490f)

# Step 2. View the generated mnemonics

Open `results.txt` with your favorite/safest editor to view the mnemonics that create the wallets you've generated.  Ideally one that does not keep history (like notepad or something)

# Step 3. View your vanityDex

`python3 vanityDex.py`

![image](https://github.com/user-attachments/assets/367772eb-c810-418e-b9a7-318efcced054)

Set a goal, try to catch all the words of a particular length, and attempt to get pretties.

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
  * `python3 vanityDex.py -l` spotting your legendaries.
* Are you a pokemaniac?
  * `python3 vanityDex.py -poke` for spotting your pokemon.
 
  
Gotta catch em all.
