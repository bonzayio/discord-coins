import datetime
from typing import Union

import discord
from discord.ext import commands

from src.helper import Helper

try:
    from src.buckethandler import BucketHandler
except:
    from buckethandler import BucketHandler


class Coins(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.coins_folder_name = 'coins'
        self.BucketHandler = BucketHandler()

        self.h = Helper()

    @commands.command(
        name=f"coins",
        brief="Gets the current coin count.",
        aliases=["getcoins"],
    )
    async def coins(self, ctx: discord.Message, user: discord.User = None) -> None:
        if ctx.channel.id != self.h.get_commands_channel_id():  # commands
            await ctx.send(f"Please use this command in the <#{self.h.get_commands_channel_id()}> channel.")
            return

        file_name = ''
        if user:
            file_name = f'{self.coins_folder_name}/{user.id}.json'
        else:
            file_name = f'{self.coins_folder_name}/{ctx.author.id}.json'

        coin_count = self.BucketHandler.get_coins(file_name)
        embed = self.h.initialize_embed('Coins')
        name = 'You'
        verb = 'have'
        if user:
            name = user.mention
            verb = 'has'
        if coin_count < 10:
            if coin_count == 1:
                embed.description = f'{name} currently {verb} **1 coin**!\n\nYou get coins for posting success into <#{self.h.get_success_channel_id()}> or posting success on Twitter and tagging `{self.h.get_twitter_mention()}`!'
            else:
                embed.description = f'{name} currently {verb} **{coin_count} coins**.\n\nYou get coins by posting success into <#{self.h.get_success_channel_id()}> or posting success on Twitter and tagging `{self.h.get_twitter_mention()}`!'
        else:
            embed.description = f'{name} currently {verb} **{coin_count} coins**.'
        await ctx.send(embed=embed)

    @commands.command(name=f"updatecoins",
                      brief="Adjusts the balance of an user",
                      aliases=["coinsupdate", "adjustcoins"],
                      usage="<USER> + or - <NUMBER>")
    @commands.has_any_role("Admin", "Administrator", "Owner")
    async def update_coins(self,
                           ctx: discord.Message,
                           user: discord.User,
                           sign: str,
                           amount: int = None) -> None:
        if ctx.channel.id != self.h.get_commands_channel_id():  # commands
            await ctx.send(f"Please use this command in the <#{self.h.get_commands_channel_id()}> channel.")
            return

        if '+' not in sign and '-' not in sign:
            embed = self.h.initialize_embed('An error has occured!')
            embed.description = f"It doesn't seem like {sign} would be either `-` nor `+`. Try again!"
            await ctx.send(embed=embed)
            return

        async def send_err():
            embed = self.h.initialize_embed('An error has occured!')
            embed.description = 'Sorry, something went wrong. Make sure you\'re using the right command and try again!'
            await ctx.send(embed=embed)

        adding = None
        value = None
        if sign == '+':
            adding = True
            value = amount
        elif sign == '-':
            adding = False
            value = amount
        elif '-' in sign:
            adding = False
            try:
                value = int(sign.replace('-', ''))
            except:
                await send_err()
                return
        else:
            adding = True
            try:
                value = int(sign.replace('+', ''))
            except:
                await send_err()
                return

        coin_count = None
        try:
            if adding:
                coin_count = self.BucketHandler.add_coins(
                    f'{self.coins_folder_name}/{user.id}.json', value)
            else:
                coin_count = self.BucketHandler.remove_coins(
                    f'{self.coins_folder_name}/{user.id}.json', value)
        except:
            await send_err()
            return

        embed = self.h.initialize_embed('Balance updated!')
        embed.description = f'{user.mention} now has **{coin_count} coins**.'

        if adding:
            embed.description += f'\n\n`{coin_count - value}` -> `{coin_count}`'
        else:
            embed.description += f'\n\n`{coin_count + value}` -> `{coin_count}`'

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Coins(client))
