import disnake
from disnake.ext import commands
from disnake import ButtonStyle, Button
import config

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '!ticket':
        embed = disnake.Embed(title="Créer un ticket", description="Cliquez sur le bouton ci-dessous pour créer un ticket.")
        components = [[Button(style=ButtonStyle.green, label="Créer un ticket", custom_id="create_ticket")]]
        message = await message.channel.send(embed=embed, components=components)
        await message.add_reaction('❌')

    await bot.process_commands(message)

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "create_ticket":
        category = interaction.guild.get_channel(config.CATEGORY_ID)
        channel = await category.create_text_channel(name=f'ticket-{interaction.author.id}')
        await channel.send(f"Bienvenue dans votre ticket, {interaction.author.mention} !")

        embed = disnake.Embed(title="Ticket", description="Ceci est un ticket.")
        components = [[Button(style=ButtonStyle.red, label="Fermer le ticket", custom_id="close_ticket")]]
        await channel.send(embed=embed, components=components)

    elif interaction.component.custom_id == "close_ticket":
        await interaction.channel.delete()

    await interaction.defer_update()

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction.message.author == bot.user and str(reaction.emoji) == '❌':
        await reaction.message.delete()

bot.run(config.TOKEN)