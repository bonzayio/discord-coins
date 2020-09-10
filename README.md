# Discord Coins Bot

Discord bot, which gives users coins for posting images (and tweets) in a certain channel.

# Features
- [x] Give coins for posting success images
- [x] Give coins for posting tweets
    - Bot checks if the tweet isn't more than a week old, if it's not a retweet and if it has your account mentioned
- [x] Commands for checking/updating coins
    - `.coins` returns how many coins you have
    - `.updatecoins @user + 10` *(Admin only)* adds balance to a user mentioned
    - `.updatecoins @user - 10` *(Admin only)* substracts balance from a user mentioned


# Setting up
You need to have Python installed for this to work.

**1.**
Change the active directory of your CMD/terminal to this folder (`cd` on Mac/Linux, `dir` on Windows)

**2.**
Run `pip install -r requirements.txt`, that will install all the dependencies.

**3.**
Set up the configuration files. Guide how to do so is [here](https://github.com/bonzayio/discord-coins/tree/master/configuration#table-of-contents)

<br></br>
**Before running, make sure you fill your info into all the files inside the configuration folder.**

**4.**
Run `python3 main.py`, that will start the bot!

# License
Licensed under the MIT License - see the [LICENSE](https://github.com/bonzayio/discord-coins/blob/master/LICENSE) file for more details.

# Author

Made by **[rtuna](https://twitter.com/rtunazzz)**.
