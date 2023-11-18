import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(error, 'original'):
            error = error.original

        await ctx.send(embed=discord.Embed(
            title=f"Error | {type(error).__name__}",
            description=str(error),
            color=0xff0000
        ))


async def setup(bot):
    await bot.add_cog(Errors(bot))
