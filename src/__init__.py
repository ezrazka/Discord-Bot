import discord
from discord.ext import commands

from .utils.misc import get_cases, get_extensions

intents = discord.Intents.default()
intents.presences = True
intents.members = True
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
    await bot.load_extension("src.cogs.commands")
    await bot.load_extension("src.cogs.errors")


@bot.command()
@commands.is_owner()
async def load(ctx, extension=None):
    if extension is None:
        extensions = get_extensions()
        for extension in extensions:
            if extension not in bot.extensions:
                await bot.load_extension(extension)
        await ctx.send(embed=discord.Embed(
            title="Success",
            description="All extensions have been successfully loaded.",
            color=0x00ff00
        ))
    else:
        await bot.load_extension(f"src.cogs.{extension}")
        await ctx.send(embed=discord.Embed(
            title="Success",
            description=f"Extension '{extension}' has been successfully loaded.",
            color=0x00ff00
        ))


@bot.command()
@commands.is_owner()
async def unload(ctx, extension=None):
    if extension is None:
        extensions = get_extensions()
        for extension in extensions:
            if extension in bot.extensions:
                await bot.unload_extension(extension)
        await ctx.send(embed=discord.Embed(
            title="Success",
            description="All extensions have been successfully unloaded.",
            color=0x00ff00
        ))
    else:
        await bot.unload_extension(f"src.cogs.{extension}")
        await ctx.send(embed=discord.Embed(
            title="Success",
            description=f"Extension '{extension}' has been successfully unloaded.",
            color=0x00ff00
        ))


@bot.command()
@commands.is_owner()
async def reload(ctx, extension=None):
    if extension is None:
        extensions = get_extensions()
        for extension in extensions:
            if extension in bot.extensions:
                await bot.unload_extension(extension)
            if extension not in bot.extensions:
                await bot.load_extension(extension)
        await ctx.send(embed=discord.Embed(
            title="Success",
            description="All extensions have been successfully reloaded.",
            color=0x00ff00
        ))
    else:
        await bot.unload_extension(f"src.cogs.{extension}")
        await bot.load_extension(f"src.cogs.{extension}")
        await ctx.send(embed=discord.Embed(
            title="Success",
            description=f"Extension '{extension}' has been successfully reloaded.",
            color=0x00ff00
        ))
