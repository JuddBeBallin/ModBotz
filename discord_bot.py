
import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="!")

def load_player_data():
    try:
        with open('players.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_player_data(player_data):
    with open('players.json', 'w') as f:
        json.dump(player_data, f, indent=4)

@bot.command()
async def login(ctx, meta_name: str, apk_version: str, modded_metadata: bool):
    player_data = load_player_data()
    discord_id = str(ctx.author.id)

    if discord_id in player_data:
        if player_data[discord_id]["meta_name"] == meta_name:
            if (player_data[discord_id]["apk_version"] == apk_version and 
                player_data[discord_id]["modded_metadata"] == modded_metadata):
                await ctx.send(f"Welcome back, {meta_name}! You are using the correct APK and metadata.")
            else:
                await ctx.send("APK version or metadata mismatch. Please verify your setup.")
        else:
            await ctx.send("Meta name mismatch. You're logged in with a different name.")
    else:
        player_data[discord_id] = {
            "meta_name": meta_name,
            "apk_version": apk_version,
            "modded_metadata": modded_metadata
        }
        save_player_data(player_data)
        await ctx.send(f"Welcome, {meta_name}! You've been registered successfully.")

@bot.command()
async def players(ctx):
    player_data = load_player_data()
    if not player_data:
        await ctx.send("No players have logged in yet.")
        return

    msg_lines = ["**Registered Players:**"]
    for discord_id, info in player_data.items():
        line = (
            f"- Meta Name: `{info['meta_name']}` | "
            f"APK Version: `{info['apk_version']}` | "
            f"Modded Metadata: `{info['modded_metadata']}`"
        )
        msg_lines.append(line)

    await ctx.send("\n".join(msg_lines))

bot.run('your_token_here')
