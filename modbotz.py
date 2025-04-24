import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="!")

# Function to load player data from the JSON file (acting as the database)
def load_player_data():
    try:
        with open('players.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save player data to the JSON file
def save_player_data(player_data):
    with open('players.json', 'w') as f:
        json.dump(player_data, f, indent=4)

# Command for logging in
@bot.command()
async def login(ctx, meta_name: str, apk_version: str, modded_metadata: bool):
    player_data = load_player_data()
    discord_id = str(ctx.author.id)  # Discord ID is unique for each user
    
    # Check if the player is already registered (if their Discord ID exists in player_data)
    if discord_id in player_data:
        if player_data[discord_id]["meta_name"] == meta_name:
            # If the Meta name matches, check if the APK version and metadata match
            if player_data[discord_id]["apk_version"] == apk_version and player_data[discord_id]["modded_metadata"] == modded_metadata:
                await ctx.send(f"Welcome back, {meta_name}! You are using the correct APK and metadata.")
            else:
                await ctx.send(f"Your APK version or metadata doesn't match the stored data. Please check again.")
        else:
            # If the Meta name doesn't match, inform the user
            await ctx.send(f"Meta name mismatch. You are already logged in with a different name.")
    else:
        # New player: Add them to the system
        player_data[discord_id] = {
            "meta_name": meta_name,  # Link the Meta/Oculus name to their Discord ID
            "apk_version": apk_version,  # Store the APK version
            "modded_metadata": modded_metadata,  # Store if they are using modded metadata
        }
        save_player_data(player_data)
        await ctx.send(f"Welcome, {meta_name}! You've been registered with APK version {apk_version}. Please ensure you're using the modded APK to access mods.")

bot.run('MTM2MzA0NTM1MzkyMTg0MzIzMA.G-QbZt.QMBjPG5vwhV8G8AFdk_rhZhGY6ja3aNcCaXXgo')