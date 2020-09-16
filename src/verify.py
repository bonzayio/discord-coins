import datetime
import json
import os
import re

import discord
import tweepy
from discord.ext import commands
from typing import Union

from src.helper import Helper
try:
    from src.buckethandler import BucketHandler
except:
    from buckethandler import BucketHandler


def check_if_url(string: str) -> bool:
    """Checks if a string passed in is an URL.

    Args:
        string (str): string to check

    Returns:
        bool: True if it is, False otherwise
    """
    regex = re.compile(
        r"^(http://www\.|https://www\.|http://|https://)?[a-z0-9]+([\-.][a-z0-9]+)*\.["
        r"a-z]{2,5}(:[0-9]{1,5})?(/.*)?$")
    return re.match(regex, string) is not None


def get_status_id(url: str) -> int:
    """Gets Twitter's status ID from an url.

    Args:
        url (str): URL to get the ID from

    Returns:
        int: The Twitter ID
    """
    x = re.findall(r"([^/]+$)", url)[0]
    if '?' in x:
        x = x.split('?')[0]
    return int(x)


class SuccessVerify(commands.Cog):
    def __init__(self, client: discord.Client):
        self.h = Helper()
        self.b = BucketHandler()
        self.SUCCESS_CHANNEL_ID = self.h.get_success_channel_id()
        self.VERIFIED_ROLE_ID = self.h.get_verified_role_id()

        # Set up Twitter API
        with open("configuration/twitter.json") as f:
            j = json.load(f)
        auth = tweepy.OAuthHandler(str(j["twitter_consumer_key"]),
                                   str(j["twitter_consumer_secret"]))
        auth.set_access_token(str(j["twitter_access_token"]),
                              str(j["twitter_access_token_secret"]))

        self.twitter_api = tweepy.API(auth)
        print('[VERIFY] Logged into Twitter.')

        self.client = client

    async def is_retweeted(self, status: tweepy.Status) -> bool:
        """Checks if a tweet is retweeted. If it is, sends an error message into Discord.

        Args:
            status (tweepy.Status): Status to check for

        Returns:
            bool: True if retweeted, False otherwise
        """
        if status.retweeted:
            embed = self.h.initialize_embed("Something went wrong!")
            embed.description = ("Uhm, this seems to be a retweet..."
                                 "Please post your own cook to get your role!")
            await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                          ).send(embed=embed)
            return True
        else:
            return False

    async def is_over_week_old(self, status: tweepy.Status) -> bool:
        """Checks if a tweet is over a week old.  If it is, sends an error message into Discord.

        Args:
            status (tweepy.Status): Status to check for

        Returns:
            bool: True if it is over a week old, False otherwise
        """
        created_at = status.created_at
        diff_date = created_at - datetime.datetime.now()
        if abs(diff_date.days) > 7:
            embed = self.h.initialize_embed("Something went wrong!")
            embed.description = (
                "Uh, oh! It seems like this tweet is over a week old."
                " Please post a more recent one to get your role!")
            await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                          ).send(embed=embed)
            return True
        else:
            return False

    async def is_account_mentioned(self, status: tweepy.Status) -> bool:
        """Checks if a tweet has an account mentioned. If it doesn't, sends an error message into Discord.

        Args:
            status (tweepy.Status): Status to check for

        Returns:
            bool: True if it does have an account mentioned, False otherwise
        """
        mention = self.h.get_twitter_mention()
        if '@' not in mention:
            mention = f'@{mention}'

        if mention not in status.full_text.lower():
            embed = self.h.initialize_embed("Something went wrong!")
            embed.description = (
                "Uh, oh! Sorry, this tweet doesn't seem to have"
                f" `{mention}` mentioned. 🧐")
            await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                          ).send(embed=embed)
            return False
        else:
            return True

    async def has_media(self, status: tweepy.Status) -> bool:
        """Checks if a tweet has any kind of media.  If it doesn't, sends an error message into Discord.

        Args:
            status (tweepy.Status): Status to check for

        Returns:
            bool: True if it has any kind of media, False otherwise
        """
        if 'media' not in status.entities.keys():
            embed = self.h.initialize_embed("Something went wrong!")
            embed.description = (
                "Sorry, this tweet doesn't seem to have any media included."
                "The media might be bad quality, or it might be a quoted retweet."
                "Re-upload and try again if that's the case! 🤪")
            await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                          ).send(embed=embed)
            return False
        else:
            return True

    async def find_verified_role(
            self, member: discord.User) -> Union[None, discord.Role]:
        """Finds the verified role specified as `self.VERIFIED_ROLE_ID`

        Returns:
            Union[None, discord.Role]: Role if found, None otherwise
        """
        verified_role = None
        for role in member.guild.roles:
            if role.id == self.VERIFIED_ROLE_ID:
                verified_role = role
        return verified_role

    async def add_salute_emoji(self, message: discord.Message) -> None:
        """Adds a salute emoji and sends a message into the success channel.

        Args:
            message (discord.Message): Discord message to react to
        """
        salute_emoji = ''
        for emoji in message.guild.emojis:
            if emoji.name.lower() == self.h.get_salute_emoji_name().lower():
                salute_emoji = emoji
        if salute_emoji:
            await message.add_reaction(salute_emoji)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != self.SUCCESS_CHANNEL_ID:
            # not in the success channel
            return

        if not check_if_url(message.content):
            return

        member = message.author
        url = message.content
        status_id = get_status_id(url)
        status = self.twitter_api.get_status(status_id, tweet_mode='extended')

        if await self.is_retweeted(status):
            print(
                f'[VERIFY] Tweet from {str(message.author)} is a retweet. Returning.'
            )
            return

        # Check if tweet is less than a week old
        if await self.is_over_week_old(status):
            print(
                f'[VERIFY] Tweet from {str(message.author)} is over a week old. Returning.'
            )
            return

        if not await self.is_account_mentioned(status):
            print(
                f'[VERIFY] Tweet from {str(message.author)} doesn\'t have our account mentioned. Returning.'
            )
            return

        if not await self.has_media(status):
            print(
                f'[VERIFY] Tweet from {str(message.author)} doesn\'t have any media. Returning.'
            )
            return

        # add coins
        current_coin_count = self.b.add_coins(
            filename=f'coins/{message.author.id}.json',
            coin_count=self.h.get_coins_for_tweet())
        embed = self.h.initialize_embed("Thanks for posting success!")
        status_message = f"Coins added! You currently have **{current_coin_count}** coins."

        verified_role = await self.find_verified_role(member)
        if not verified_role:
            print("[VERIFY] Failed to find the verify role.")

        if verified_role in member.roles:
            print(f"[VERIFY] User {member} already has the verified role.")

        if verified_role not in member.roles:
            status_message += '\n\nI also added you the Verified role! Keep cooking. 👨‍🍳'
            try:
                await member.add_roles(verified_role,
                                       reason="Posted success on Twitter.")
            except discord.errors.Forbidden:
                print(
                    "[VERIFY] Not enough permissions to give the user a verify role!"
                )

        embed.description = status_message
        await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                      ).send(embed=embed)

        await self.add_salute_emoji(message)
        return


def setup(client):
    client.add_cog(SuccessVerify(client))
