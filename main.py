import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from discord.ext.commands.errors import CommandInvokeError



token = open('configuration/discord-token.txt').read()

if 'DYNO' in os.environ:
    print("[MAIN] - Running on HEROKU")
else:
    print("[MAIN] - Running on LOCAL")

client = commands.Bot(command_prefix='.')
client.remove_command('help')

print("******************** Trying to load Cogs ********************")
for filename in os.listdir('./src'):

    if filename == '__init__.py':
        continue
    if filename == 'helper.py':
        continue
    if filename == 'buckethandler.py':
        continue

    if filename.endswith(".py"):
        print(f"[MAIN] - Trying to load {filename}.")
        try:
            client.load_extension(f"src.{filename[:-3]}")
        except Exception as e:
            print(
                f"[MAIN] ERROR - Failed to load cog named {filename}. Error: {e}"
            )
print("******************** Loaded Cogs ********************")

if 'DYNO' in os.environ:

    @client.event
    async def on_command_error(ctx: discord.Message, error):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("Some arguments are wrong or missing.")
            return
        else:
            await ctx.send('Sorry, an error has occured. Please try again!')
        print(
            f"[MAIN] - An error has occurred while using command {ctx.command.cog_name}: {error}"
        )


@client.event
async def on_ready() -> None:
    print(f"[MAIN] - We have logged in as {client.user}")
    await client.change_presence(
        activity=discord.Activity(name=f"over success posts!", type=3))


client.run(token)