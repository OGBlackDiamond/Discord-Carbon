import discord
import time
import os
from discord.ext import commands
from discord.message import Message

from config_util import ConfigUtil
from email.email_util import EmailUtil

intents = discord.Intents.default()
intents.message_content = True;

client = commands.Bot(command_prefix=".", intents=intents)
start_time = time.time()

config = ConfigUtil()
gmail_util = EmailUtil(config.get_email_config()["from"], config.get_email_config()["password"])

@client.tree.command(name='info', description="Sends a message containing all of the info about this bot.")
async def info(interaction: discord.Interaction):
    uptime = time.time() - start_time

    days = (uptime / 86400).__floor__() 
    uptime %= 86400
    hours = (uptime / 3600).__floor__() 
    uptime %= 3600
    minutes = (uptime / 60).__floor__() 
    uptime %= 60
    seconds = (uptime).__floor__()

    uptime_string = f"Online for: {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"

    await interaction.response.send_message(f"Carbon created by BlackDiamond\n\nRunning on server: {os.uname().nodename}\n{uptime_string}")

@client.event
async def on_message(message: Message):

    if message.author == client.user: return

    # memes stuff
    if message.content.startswith("echo"):
        await message.channel.send(message.content[5:])
        return

    if message.content.lower() == "you are carbon":
        await message.channel.send("I am Carbon")
        return

    if message.content.lower() == "you will create the perfect system":
        await message.channel.send("I will create the perfect system")
        return

    # emails stuff
    if message.content.startswith(f"<@&{config.get_email_config().get("email_role")}>"):
        await gmail_util.parse_message(message, config.get_email_config())
        return

        




@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.tree.sync()
    print("Synced the command tree!")


bot_token = config.get_base_config().get("bot_token")
if bot_token == None:
    print("No bot token found!")
    quit()
client.run(bot_token)

