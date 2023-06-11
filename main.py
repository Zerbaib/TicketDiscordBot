import disnake
from disnake.ext import commands
from disnake.ui import Button, Select
import config

intents = disnake.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot('!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity=disnake.Activity(
        type=disnake.ActivityType.watching,
        name=f'{members} members'
    ))
    print('Ready to support ✅')

class TicketView(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(label="Create a ticket", style=disnake.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(
            embed=None,
            components=[],
        )

        channel = interaction.channel
        category = interaction.guild.get_channel(config.CATEGORY_ID)
        channel = await category.create_text_channel(name=f'ticket-{interaction.author.id}')
        await channel.send(f"Welcome to your ticket, {interaction.author.mention}!")

        embed = disnake.Embed(title="Ticket", description="This is a ticket.")
        components = [
            [
                Button(style=disnake.ButtonStyle.red, label="Close ticket", custom_id="close_ticket")
            ]
        ]
        await channel.send(embed=embed, components=components)

    @disnake.ui.button(label="Close ticket", style=disnake.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(
            content=f"Ticket closed by {interaction.author.mention}.",
            embed=None,
            components=[],
        )
        await interaction.channel.delete()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '!ticket':
        embed = disnake.Embed(title="Create a ticket", description="Click the button below to create a ticket.")
        view = TicketView()
        await message.channel.send(embed=embed, view=view)
        await message.add_reaction('❌')

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.message.author == bot.user and str(reaction.emoji) == '❌':
        await reaction.message.delete()

bot.run(config.TOKEN)
