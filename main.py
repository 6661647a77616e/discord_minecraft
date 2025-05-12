import discord
from discord import app_commands
from discord.ext import commands
import minestat
import random
import logging
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
java_address = os.getenv("JAVA_ADDRESS")
port = int(os.getenv("PORT"))
bot_token = os.getenv("DISCORD_BOT_TOKEN")

# Configure logging
logging.basicConfig(
    filename='log.txt',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Setup Discord bot
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
        logging.error(f"Failed to sync commands: {e}")

@tree.command(name="player", description="Check how many players are online in the Minecraft server.")
async def player(interaction: discord.Interaction):
    user = interaction.user
    try:
        ms = minestat.MineStat(java_address, port)

        if not ms.online:
            message = "❌ Server is offline or not responding. 💤"
            await interaction.response.send_message(message, delete_after=300)
            logging.info(f"/player by {user}: {message}")
            return

        count = int(ms.current_players)
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

        await interaction.response.send_message(message, delete_after=300)
        logging.info(f"/player by {user}: {message}")

    except Exception as e:
        error_message = f"⚠️ Unexpected error: {str(e)}"
        await interaction.response.send_message(error_message, delete_after=300)
        logging.error(f"/player by {user}: {error_message}")

@tree.command(name="status", description="Check if the Minecraft server is online.")
async def status(interaction: discord.Interaction):
    user = interaction.user
    try:
        ms = minestat.MineStat(java_address, port)

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

        await interaction.response.send_message(message, delete_after=300)
        logging.info(f"/status by {user}: {message}")

    except Exception as e:
        error_message = f"⚠️ Unexpected error: {str(e)}"
        await interaction.response.send_message(error_message, delete_after=300)
        logging.error(f"/status by {user}: {error_message}")

bot.run(bot_token)
