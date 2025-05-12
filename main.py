import discord
from discord import app_commands
from discord.ext import commands
import minestat
import random
import asyncio
import logging
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
JAVA_ADDRESS = os.getenv("JAVA_ADDRESS")
PORT = int(os.getenv("PORT", "25565"))

# External test server
TEST_ADDRESS = "best.fadecloud.com"
TEST_PORT = 19132

# Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"⚠️ Failed to sync commands: {e}")

# /player command
@tree.command(name="player", description="Check how many players are online in the Minecraft server.")
async def player(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        ms = minestat.MineStat(JAVA_ADDRESS, PORT)
        user = interaction.user

        if ms.online:
            count = ms.current_players
            if count == 0:
                message = (
                    "😶 Hmm, there’s no cubers online… Might as well invite them.\n"
                    "📣 Tell them to stop working too hard and play some games! 🎮"
                )
            else:
                responses = [
                    f"🎉 Hooray! {count} player(s) online!",
                    f"👀 Stop bothering me, go bother {count} person(s) on the server!",
                    f"🔥 The blocky world has {count} explorer(s) right now!",
                    f"🌍 There's a gathering of {count} cube-head(s)!",
                    f"😎 {count} people are crafting their destinies online!",
                    f"🧱 Whoa! {count} brick lovers online!",
                    f"💻 Server buzzin’ with {count} player(s)! Join in!"
                ]
                message = random.choice(responses)
        else:
            message = "❌ Server is offline or not responding. 💤"

        msg = await interaction.followup.send(message)
        logging.info(f"/player by {user}: {message}")
        await asyncio.sleep(300)
        await msg.delete()

    except Exception as e:
        error_message = f"⚠️ Unexpected error: {str(e)}"
        msg = await interaction.followup.send(error_message)
        logging.error(f"/player by {interaction.user}: {error_message}")
        await asyncio.sleep(300)
        await msg.delete()

# /status command
@tree.command(name="status", description="Check if the Minecraft server is online.")
async def status(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        ms = minestat.MineStat(JAVA_ADDRESS, PORT)
        user = interaction.user

        if ms.online:
            responses = [
                "🟢 Server is alive and kicking!",
                "🎮 All systems go — time to play!",
                "🌟 The server is up! Get your pickaxe ready!",
                "💡 Green light — server's online!",
                "🏰 The realm awaits — server is running fine!"
            ]
            message = random.choice(responses)
        else:
            message = "🔴 Server is offline or unreachable at the moment. Try again later."

        msg = await interaction.followup.send(message)
        logging.info(f"/status by {user}: {message}")
        await asyncio.sleep(300)
        await msg.delete()

    except Exception as e:
        error_message = f"⚠️ Unexpected error: {str(e)}"
        msg = await interaction.followup.send(error_message)
        logging.error(f"/status by {interaction.user}: {error_message}")
        await asyncio.sleep(300)
        await msg.delete()

# /test command
@tree.command(name="test", description="Test network by pinging an external Minecraft server.")
async def test(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        main_server = minestat.MineStat(JAVA_ADDRESS, PORT)
        test_server = minestat.MineStat(TEST_ADDRESS, TEST_PORT)
        user = interaction.user

        if not main_server.online and test_server.online:
            message = (
                "🧪 Test complete!\n"
                f"🔴 Your server (`{JAVA_ADDRESS}:{PORT}`) is **offline**.\n"
                f"🟢 But the test server (`{TEST_ADDRESS}:{TEST_PORT}`) is **online**.\n"
                "❗ This might indicate an issue with **your Minecraft server** configuration."
            )
        elif not main_server.online and not test_server.online:
            message = (
                "🧪 Test complete!\n"
                f"🔴 Both your server (`{JAVA_ADDRESS}:{PORT}`) and the test server (`{TEST_ADDRESS}:{TEST_PORT}`) are offline.\n"
                "📶 This might be a **network issue** on your side. Check your internet connection."
            )
        elif main_server.online and test_server.online:
            message = (
                "🧪 Test complete!\n"
                f"✅ Both servers are **online**!\n"
                "🎉 Looks like everything is working perfectly."
            )
        else:
            message = "⚠️ Unexpected result while testing. Try again later."

        msg = await interaction.followup.send(message)
        logging.info(f"/test by {user}: {message}")
        await asyncio.sleep(300)
        await msg.delete()

    except Exception as e:
        error_message = f"⚠️ Unexpected error during /test: {str(e)}"
        msg = await interaction.followup.send(error_message)
        logging.error(f"/test by {interaction.user}: {error_message}")
        await asyncio.sleep(300)
        await msg.delete()

bot.run(BOT_TOKEN)
