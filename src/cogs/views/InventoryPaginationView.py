import discord
import discord.ui
import math


class InventoryPaginationView(discord.ui.View):
    def __init__(self, ctx, owned_pokemon, n_per_page=8, *, timeout=3 * 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.owned_pokemon = owned_pokemon
        self.n_pokemon = len(owned_pokemon)
        self.n_per_page = n_per_page
        self.n_pages = math.ceil(self.n_pokemon / self.n_per_page)
        self.current_page = 0
        self.pages = self.get_pages()

        self.disable_buttons()

    def get_pages(self):
        pages = []

        if self.n_pages == 0:
            return [discord.Embed(
                title=f"{self.ctx.author.name}'s Inventory",
                description=f"This user currently has no pokemon!",
                color=0xffff00
            )]

        for i in range(self.n_pages):
            lower_bound = i * self.n_per_page + 1
            upper_bound = min((i + 1) * self.n_per_page, self.n_pokemon)

            embed = discord.Embed(
                title=f"{self.ctx.author.name}'s Inventory",
                description=f"Displaying entries {lower_bound}-{upper_bound}",
                color=0xffff00
            )
            for j in range(lower_bound - 1, upper_bound):
                pokemon_name, count = list(self.owned_pokemon.items())[j]
                embed.add_field(
                    name=f"{pokemon_name.title()} `x{count}`",
                    value="",
                    inline=False
                )
            pages.append(embed)

        return pages

    def disable_buttons(self):
        first_button = self.children[0]
        prev_button = self.children[1]
        next_button = self.children[2]
        last_button = self.children[3]

        first_button.disabled = self.n_pages <= 1 or self.current_page == 0
        prev_button.disabled = self.n_pages <= 1
        next_button.disabled = self.n_pages <= 1
        last_button.disabled = self.n_pages <= 1 or self.current_page == self.n_pages - 1

    async def check_author(self, interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(label="<<", style=discord.ButtonStyle.primary)
    async def first(self, interaction, button):
        if not await self.check_author(interaction):
            return

        self.current_page = 0
        new_page = self.pages[self.current_page]
        self.disable_buttons()
        await interaction.response.edit_message(embed=new_page, view=self)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev(self, interaction, button):
        if not await self.check_author(interaction):
            return

        self.current_page = (self.current_page - 1) % self.n_pages
        new_page = self.pages[self.current_page]
        self.disable_buttons()
        await interaction.response.edit_message(embed=new_page, view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next(self, interaction, button):
        if not await self.check_author(interaction):
            return

        self.current_page = (self.current_page + 1) % self.n_pages
        new_page = self.pages[self.current_page]
        self.disable_buttons()
        await interaction.response.edit_message(embed=new_page, view=self)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.primary)
    async def last(self, interaction, button):
        if not await self.check_author(interaction):
            return

        self.current_page = self.n_pages - 1
        new_page = self.pages[self.current_page]
        self.disable_buttons()
        await interaction.response.edit_message(embed=new_page, view=self)
