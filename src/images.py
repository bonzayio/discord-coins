import datetime
import random
import string

import discord
from discord.ext import commands

from src.helper import Helper
try:
    from src.buckethandler import BucketHandler
except:
    from buckethandler import BucketHandler

class Success(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.h = Helper()
        self.b = BucketHandler()

        self.coins_folder_name = 'coins'
        self.SUCCESS_CHANNEL_ID = self.h.get_success_channel_id()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != int(self.SUCCESS_CHANNEL_ID):
            # not in the success channel
            return

        if not message.attachments:
            #  no images
            return

        mention = self.h.get_twitter_mention()
        if '@' not in mention:
            mention = f'@{mention}'

        current_coin_count = self.b.add_coins(filename=f'{self.coins_folder_name}/{message.author.id}.json', coin_count=self.h.get_coins_for_picture())
        embed = self.h.initialize_embed(f"Coins added!")
        if current_coin_count == 1:
            embed.description = f"You now have **{current_coin_count} coin**!\n\nMake sure to post on Twitter and tag us (`{mention}`)!"
        else:
            embed.description = f"You now have **{current_coin_count} coins**!\n\nMake sure to post on Twitter and tag us (`{mention}`)!"
        
        await self.client.get_channel(id=self.SUCCESS_CHANNEL_ID
                                      ).send(embed=embed)


def setup(client):
    client.add_cog(Success(client))
