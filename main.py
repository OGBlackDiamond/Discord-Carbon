import discord
import time
import os
from discord.ext import commands
from discord.message import Message

from util.config_util import ConfigUtil
from util.gmail_util import GmailUtil

intents = discord.Intents.default()
intents.message_content = True;

client = commands.Bot(command_prefix=".", intents=intents)
start_time = time.time()

config = ConfigUtil()
gmail_util = GmailUtil(config.get_config()["from"], config.get_config()["password"])

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

    uptime_string = f"Bot online for: {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"

    await interaction.response.send_message(f"Bot running on server: {os.uname().nodename}\n{uptime_string}")

@client.event
async def on_message(message: Message):

    if message.author == client.user:
        return

    if message.content.startswith("echo"):
        await message.channel.send(message.content[5:])
        return

    if message.content.lower() == "you are carbon":
        await message.channel.send("I am Carbon")
        return

    if message.content.lower() == "you will create the perfect system":
        await message.channel.send("I will create the perfect system")
        return

    if message.content.startswith(f"<@&{config.get_config().get("email_role")}>"):
        if (message.content[23:24] == " "):
            start_index = 24
        else:
            start_index = 23
        
        authorize_email = False
        for guild in config.get_config().get("email_server_list"): #type: ignore
            if message.guild.id == guild: # type: ignore
                authorize_email = True
                break

        if not authorize_email:
            await message.channel.send("This server is not authorized to send email notifications!")
            return

        name = message.author.nick
        if name == None:
            name = message.author.name

        await message.channel.send("Talking to Email api...")
        for recipient in config.get_config().get("email_recipients"): #type: ignore
            gmail_util.send_message(recipient, name, message.content[start_index:]) #type: ignore
            await message.channel.send(content="Message failed to send!")
            return


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.tree.sync()
    print("Synced the command tree!")


bot_token = config.get_config().get("bot_token")
if bot_token == None:
    print("No bot token found!")
    quit()
client.run(bot_token)

