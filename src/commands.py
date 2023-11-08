from . import commands, bot


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Commands(bot))


@bot.command()
@commands.is_owner()
async def say(ctx, message):
    await ctx.send(message)
