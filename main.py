import discord
import os
from discord.ext import commands
from discord.message import Message

from util.config_util import ConfigUtil

intents = discord.Intents.default()
intents.message_content = True;

client = commands.Bot(command_prefix=".", intents=intents)

config = ConfigUtil()

@client.tree.command(name='info', description="Sends a message containing all of the info about this bot.")
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bot running on server: {os.uname().nodename}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.tree.sync()
    print("Synced the command tree!")

@client.event
async def on_message(message: Message):
    print(f"Message from {message.author}: {message.content}")

    if message.author == client.user:
        return

    if message.content.startswith("echo"):
        await message.channel.send(message.content[5:])

bot_token = config.get_config().get("bot_token")
if bot_token == None:
    print("No bot token found!")
    quit()
client.run(bot_token)

