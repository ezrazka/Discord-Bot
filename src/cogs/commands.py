import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import json
import os
import random
import math

from .. import bot
from ..views.InventoryPaginationView import InventoryPaginationView
from ..utils.database import add_user, add_pokemon, exists_user, get_owned_pokemon


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
            cmd.name for cmd in sorted(self.bot.commands) if not has_is_owner_check(cmd)
        ]

        await ctx.send(embed=discord.Embed(
            title="Commands",
            description=", ".join(command_list),
            color=0xff00ff
        ))

    @commands.command()
    # @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def roll(self, ctx):
        description = None
        footer = None
        with open("src/data/json/pokemon.json", "r") as f:
            data = json.load(f)
            pokemon_name = random.choice(list(data.keys()))
            data = data[pokemon_name]

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
        discord_id = ctx.author.id
        owned_pokemon = get_owned_pokemon(discord_id)

        owned_pokemon_dict = {}
        for pokemon in owned_pokemon:
            if pokemon[2] not in owned_pokemon_dict.keys():
                owned_pokemon_dict[pokemon[2]] = 1
            else:
                owned_pokemon_dict[pokemon[2]] += 1

        if len(owned_pokemon_dict) == 0:
            return await ctx.send("You currently have no pokemon!")

        view = InventoryPaginationView(ctx, owned_pokemon_dict)
        await ctx.send(embed=view.pages[0], view=view)


async def setup(bot):
    await bot.add_cog(Commands(bot))
