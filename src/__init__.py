import discord
from discord.ext import commands

from utils import get_cases

intents = discord.Intents.default()
intents.message_content = True

DEFAULT_PREFIX = "!"
PREFIX = DEFAULT_PREFIX

bot = commands.Bot(
    command_prefix=get_cases(PREFIX),
    owner_id=1012689630480580719,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
    intents=intents
)

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(
            name=f"{DEFAULT_PREFIX}help"
        )
    )

bot.load_extension("data.commands")


@bot.command()
@commands.is_owner()
async def load(ctx):
    try:
        await bot.load_extension("src.commands")
        await ctx.reply("All commands have been successfully loaded.")
    except Exception as e:
        print(f"Failed to load extension: {e}")


@bot.command()
@commands.is_owner()
async def unload(ctx):
    try:
        await bot.unload_extension("src.commands")
        await ctx.reply("All commands have been successfully unloaded.")
    except Exception as e:
        print(f"Failed to unload extension: {e}")


@bot.command()
@commands.is_owner()
async def reload(ctx):
    try:
        await bot.unload_extension("src.commands")
        await bot.load_extension("src.commands")
        await ctx.reply("All commands have been successfully reloaded.")
    except Exception as e:
        print(f"Failed to reload extension: {e}")
