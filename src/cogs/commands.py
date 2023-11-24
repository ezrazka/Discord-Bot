import discord
from discord.ext import commands
import asyncio
import json
import re
import random

from .. import bot
from .views.InventoryPaginationView import InventoryPaginationView
from ..utils.database import add_user, add_pokemon, exists_user, get_owned_pokemon
from ..utils.misc import parse_time, get_image_file


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        discord_id = ctx.author.id
        if not exists_user(discord_id):
            add_user(discord_id)

    @commands.command(brief="[command name]", description="Get information on what commands are available, and what they do.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, command_name=None):
        if command_name is not None:
            command_name = command_name.lower().strip()
            command = bot.get_command(command_name)

            if command is None or any(commands.is_owner()(check) for check in command.checks):
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(
                    title="Oops!",
                    description=f"No command named '{command_name}'.",
                    color=0x000000
                ))

            if command.brief == "":
                usage = f"{ctx.prefix}{command.name}"
            else:
                usage = f"{ctx.prefix}{command.name} {command.brief}"
            description = command.description
            cooldown = command.cooldown.per

            embed = discord.Embed(
                title=f"Command: `{ctx.prefix}{command.name}`",
                description=f"""
                **Usage:** `{usage}`
                **Description:** {description}
                **Cooldown:** {parse_time(int(cooldown))}
                """,
                color=0xff00ff
            )
            embed.set_footer(text="Usage Syntax: <required> [optional]")

            return await ctx.send(embed=embed)

        def has_is_owner_check(command):
            return any(commands.is_owner()(check) for check in command.checks)

        command_list = [
            cmd.name for cmd in sorted(self.bot.commands, key=lambda x: x.name) if not has_is_owner_check(cmd)
        ]

        embed = discord.Embed(
            title="Commands",
            description=f"Type `{ctx.prefix}<command name>` for further information.",
            color=0xff00ff
        )
        embed.add_field(
            name="Commands:",
            value=", ".join(command_list)
        )

        await ctx.send(embed=embed)

    @commands.command(brief="", description="Roll for a Pokémon! Type `catch <pokémon name>` to catch them, but beware, guessing their name incorrectly will cause them to flee.")
    @commands.cooldown(1, 5 * 60, commands.BucketType.user)
    async def roll(self, ctx):
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
                sprite_file = get_image_file(
                    data["sprites"]["normal"], "pokemon.png", size=2)
            else:
                sprite_file = get_image_file(
                    data["sprites"]["shiny"], "pokemon.png", size=2)
                footer = "This Pokémon looks odder than usual! ✨"

        random_hex_color = random.randrange(0xffffff)
        embed = discord.Embed(
            title="A wild Pokémon appeared!",
            description="Type `catch <pokémon name>` to catch it!",
            color=random_hex_color
        )
        embed.set_image(url="attachment://pokemon.png")
        embed.set_footer(text=footer)
        await ctx.send(embed=embed, file=sprite_file)

        def check(msg):
            return msg.author.id == ctx.author.id and msg.content.split()[0].lower() == "catch"

        try:
            message = await bot.wait_for('message', timeout=15, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(embed=discord.Embed(
                title="You Took Too Long!",
                description=f"The opposing {pokemon_name.title()} fled away!",
                color=0x00ffff
            ))

        guess = " ".join(message.content.split()[1:]).lower().strip()
        if guess == pokemon_name:
            discord_id = message.author.id

            add_pokemon(discord_id, pokemon_name, ability, is_shiny)

            return await ctx.send(embed=discord.Embed(
                description=f"{pokemon_name.title()} was successfully caught by {message.author.mention}!",
                color=0x00ff00
            ))
        else:
            return await ctx.send(embed=discord.Embed(
                title="You Guessed Incorrectly!",
                description=f"The opposing {pokemon_name.title()} fled away!",
                color=0x00ffff
            ))

    @commands.command(brief="[user id | user mention]", description="Check your own or another's Pokémon inventory.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def inventory(self, ctx, user=None):
        if user is None:
            discord_id = ctx.author.id
        elif user.isdigit():
            discord_id = int(user)
        elif re.match(r"<@(\d+)>", user):
            discord_id = int(user[2:-1])
        else:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                title="Oops!",
                description="You must input a user ID or mention a user.",
                color=0x000000
            ))

        inventory_user = bot.get_guild(ctx.guild.id).get_member(discord_id)
        if inventory_user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                title="Oops!",
                description=f"Could not recognize user with id '{discord_id}'.",
                color=0x000000
            ))

        owned_pokemon = get_owned_pokemon(discord_id)

        owned_pokemon_dict = {}
        for pokemon in owned_pokemon:
            if pokemon[2] not in owned_pokemon_dict.keys():
                owned_pokemon_dict[pokemon[2]] = 1
            else:
                owned_pokemon_dict[pokemon[2]] += 1

        view = InventoryPaginationView(ctx, inventory_user, owned_pokemon_dict)
        await ctx.send(embed=view.pages[0], view=view)

    @commands.command(brief="<pokémon name>", description="Get information surrounding a specific Pokémon.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def info(self, ctx, pokemon_name=None):
        if pokemon_name is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                title="Oops!",
                description="You must input a Pokémon name.",
                color=0x000000
            ))

        pokemon_name = pokemon_name.lower().strip()

        with open("src/data/json/pokemon.json", "r") as f:
            data = json.load(f)

            if pokemon_name not in data:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(
                    title="Oops!",
                    description=f"No Pokémon named {pokemon_name.title()}.",
                    color=0x000000
                ))

            pokemon_data = data[pokemon_name]

        base_stats = pokemon_data["base_stats"]
        sprite_file = get_image_file(
            pokemon_data["sprites"]["normal"], f"{pokemon_name}.png", size=2)
        abilities = []
        for ability in pokemon_data["abilities"]["normal"]:
            abilities.append(ability)
        for ability in pokemon_data["abilities"]["hidden"]:
            abilities.append(ability)

        embed = discord.Embed(
            title=f"#{pokemon_data['id']:0>3} — {pokemon_name.title()}",
            description=f"""
            **HP:** {base_stats['hp']}
            **Attack:** {base_stats['attack']}
            **Defense:** {base_stats['defense']}
            **Special Attack:** {base_stats['special-attack']}
            **Special Defense:** {base_stats['special-defense']}
            **Speed:** {base_stats['speed']}
            **Base Stat Total:** {sum(map(int, base_stats.values()))}
            """,
            color=0xff00ff
        )
        embed.add_field(
            name="Height",
            value=f"{pokemon_data['height'] / 10} m"
        )
        embed.add_field(
            name="Weight",
            value=f"{pokemon_data['weight'] / 10} kg"
        )
        embed.add_field(
            name="Types",
            value=", ".join(map(lambda x: x.title(), pokemon_data["types"]))
        )
        embed.add_field(
            name="Abilities",
            value=", ".join(map(lambda x: x.title(), abilities)),
            inline=False
        )
        embed.set_thumbnail(url=f"attachment://{pokemon_name}.png")
        embed.set_footer(
            text="Credits to https://pokeapi.co",
            icon_url="https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png"
        )

        await ctx.send(embed=embed, file=sprite_file)


async def setup(bot):
    await bot.add_cog(Commands(bot))
