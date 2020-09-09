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
    async def coins(self, ctx: discord.Message) -> None:
        if ctx.channel.id != self.h.get_commands_channel_id():  # commands
            await ctx.send("Please use this command in the #commands channel.")
            return

        coin_count = self.BucketHandler.get_coins(
            f'{self.coins_folder_name}/{ctx.author.id}.json')
        embed = self.h.initialize_embed('Coins')
        if coin_count < 10:
            if coin_count == 1:
                embed.description = f'You currently have **1 coin**!\n\nYou get coins for posting your success into <#594130475199627264> or posting success on Twitter and tagging `bonzayio`!'
            else:
                embed.description = f'You currently have **{coin_count} coins**.\n\nYou get coins for posting your success into <#594130475199627264> or posting success on Twitter and tagging `bonzayio`!'

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
            await ctx.send("Please use this command in the #commands channel.")
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
                send_err()
                return
        else:
            adding = True
            try:
                value = int(sign.replace('+', ''))
            except:
                send_err()
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
            send_err()
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
