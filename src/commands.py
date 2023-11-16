import discord
from discord.ext import commands
import asyncio
import os
import json
import random

from . import bot
from utils.database import add_user, add_pokemon, exists_user


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        discord_id = ctx.author.id
        if not exists_user(discord_id):
            add_user(discord_id)

    @commands.command()
    # @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def help(self, ctx):
        def has_is_owner_check(command):
            return any(commands.is_owner()(check) for check in command.checks)

        command_list = [
            cmd.name for cmd in self.bot.commands if not has_is_owner_check(cmd)
        ]

        await ctx.send(embed=discord.Embed(
            title="Commands",
            description=", ".join(command_list),
            color=0xff00ff
        ))

    @commands.command()
    # @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def roll(self, ctx):
        json_dir = "data/json/"
        json_files = os.listdir(json_dir)
        pokemon_json = random.choice(json_files)
        pokemon_name = pokemon_json[:-5]

        description = None
        footer = None
        pokemon_json_dir = f"{json_dir}/{pokemon_json}"
        with open(pokemon_json_dir, "r") as f:
            data = json.load(f)

            if random.randint(1, 128) > 1 or not data["abilities"]["secret"]:
                ability = random.choice(data["abilities"]["normal"])
            else:
                ability = random.choice(data["abilities"]["secret"])

            is_shiny = random.randint(1, 128) > 1
            if is_shiny:
                pokemon_image = data["sprites"]["normal"]
            else:
                pokemon_image = data["sprites"]["shiny"]
                footer = "This pokemon looks odder than usual! ✨"

        file = discord.File(pokemon_image, filename="pokemon.png")
        random_hex_color = random.randint(0, 0xffffff)
        embed = discord.Embed(
            title="A wild Pokémon appeared!",
            description=description,
            color=random_hex_color
        )
        embed.set_image(url="attachment://pokemon.png")
        embed.set_footer(text=footer)
        await ctx.send(embed=embed, file=file)

        def check(msg):
            return not msg.author.bot and msg.content.split()[0].lower() == "catch"

        try:
            message = await bot.wait_for('message', timeout=5, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(embed=discord.Embed(
                title="Timeout",
                description="The opposing pokemon fled away!",
                color=0x00ffff
            ))

        guess = " ".join(message.content.split()[1:]).lower().strip()
        if guess == pokemon_name:
            discord_id = message.author.id
            if not exists_user(discord_id):
                add_user(discord_id)
            add_pokemon(discord_id, pokemon_name, ability, is_shiny)

            return await ctx.send(embed=discord.Embed(
                description=f"{pokemon_name.title()} was successfully caught by {message.author.mention}!",
                color=0x00ff00
            ))
        else:
            return await ctx.send(embed=discord.Embed(
                title="Incorrect Guess",
                description="The opposing pokemon fled away!",
                color=0x00ffff
            ))

    @commands.command()
    # @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def inventory(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(Commands(bot))
