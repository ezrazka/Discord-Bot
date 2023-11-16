import discord
from discord.ext import commands

from utils.misc import get_cases

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
    await bot.load_extension("src.commands")


@bot.command()
@commands.is_owner()
async def load(ctx):
    await bot.load_extension("src.commands")
    await ctx.reply("All commands have been successfully loaded.")


@bot.command()
@commands.is_owner()
async def unload(ctx):
    await bot.unload_extension("src.commands")
    await ctx.reply("All commands have been successfully unloaded.")


@bot.command()
@commands.is_owner()
async def reload(ctx):
    await bot.unload_extension("src.commands")
    await bot.load_extension("src.commands")
    await ctx.reply("All commands have been successfully reloaded.")
