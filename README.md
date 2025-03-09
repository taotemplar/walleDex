# WalleDex
### A vanity wallet generator game for Bittensor.  Collect rare words, build your WalleDex, and increase your vanity!

![image](https://github.com/user-attachments/assets/f5d2b82c-50d4-4c3b-9cd5-e8a85c54bd78)



### Gotta hash em all!

Quick overview: 
- `generateWallets.py` generates new wallets/mnemonics and saves the results into `rawAddresses.txt`
  - It searches for any word in `words.txt`, and checks if any of those words occur in the 1st, 2nd, and 3rd characters in the wallet address.
- `walleDex.py` allows you to look at your generated addresses and their statistics

# Step 0. Installation
Clone this repo

```
git clone https://github.com/taotemplar/walleDex.git
```

Install virtualenv

```
pip3 install virtualenv
virtualenv ~/.venvs/walleDex
```

Activate and install virtual env requirements

```
source ~/.venvs/walleDex/bin/activate
cd walleDex
pip install -r requirements.txt
```



# Step 1. Run the generator

```
python3 generateWallets.py
```

![image](https://github.com/user-attachments/assets/de890bbd-5056-4ab0-913a-57c69d8a91a9)


Wallets are printed to console and their key/mnemonics are stored in `rawAddresses.txt`.  Can close with ctrl+c, and resume by re-running `python3 generateWallets.py` again.

Tip: `python3 generateWallets.py --help` for parameters to change what wallets are saved.


# Step 2. View the generated mnemonics

Open `rawAddresses.txt` with your favorite/safest editor to view the mnemonics that create the wallets you've generated.  Ideally open with an editor that does not keep history (notepad would be safe)

# Step 3. View your WalleDex

```
python3 walleDex.py
```

![image](https://github.com/user-attachments/assets/96cb2e75-3353-48d9-ba06-5dbd72634247)

![image](https://github.com/user-attachments/assets/2553c4be-4fa8-437e-9a47-0bb6c78ee132)

Set a goal, try to catch all the words of a particular length, and attempt to get pretties.

Tip: `python3 walleDex.py --help` to view wallets and filtering options

# Step 4. The game

Not everyone's path or goals are the same.  You can carve your own goals.

Here are some ideas:

* Do you want to hash em all?  Try filling out the 3 letter words, then work on the 4 letter words, etc.
  * `python3 generateWallets.py -n=4`
    * `-n` parameter sets the minimum word length.  Increase as needed
* Do you only want to catch long worded wallets?
  * `python3 generateWallets.py -n=6`
    * `-n` parameter is helpful here again, probably with a minimum of 5.
* Do you only want to catch pretty worded wallets?
  * `python3 generateWallets.py -p`
    * `-p` parameter only looks for words that are --pretty.  Eg: ALLUPPERCASE or alllowercase or Startwithacapital.
* What about legendary wallets?
  * Legendary wallets are those that have more than 1 word, the word may be after the first word in the address OR at the end of the wallet address.
    * Eg: 5**FIRE**xlkc...3ud**SALT**
  * `python3 walleDex.py -l` for spotting your legendaries.
* Are you a pokemaniac?
  * `python3 walleDex.py -poke` for spotting your pokemon.

# Step 5. rawAddresses.txt size
* But be wary of your `rawAddresses.txt` size.  It can grow fast if you don't use parameters with `python3 generateWallets.py` !

# Step 6. Actually using the wallet
* Never copy a mnemonic from `rawAddresses.txt` to your clipboard, never save it outside of the file.
* Physically write the mnemonic of the wallet you want to use to a piece of paper outside of your computer.  Then write it down again (2 pieces of paper).  See 44:44 here in this video for a run-down of how to safely store a mnemonic https://youtu.be/UH_sOZSIk10?t=2688 .
* DELETE the wallet's mnemonic from the `rawAddresses.txt` file.  Save and close the file.
* Then manually type in the mnemonic to your favorite wallet app by looking at your paper mnemonic.

# Step 7. Show it off
* For maximum vanity, send a tiny donation to the "showme" wallet
* This wallet's received transfers serves as the place to show off the best vanity wallets:
  * https://taostats.io/account/5GshoWMe6a9AgoqBGBnkBG1sy2ygvdqHhaMtP2qEKiWhq8Xn/transfers
