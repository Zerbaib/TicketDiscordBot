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
        button = Button(style=ButtonStyle.green, label="Créer un ticket", custom_id="create_ticket")
        embed = disnake.Embed(title="Panel de création de ticket", description="Cliquez sur le bouton ci-dessous pour créer un ticket.")
        await message.channel.send(embed=embed, components=[[button]])

    await bot.process_commands(message)

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "create_ticket":
        category = interaction.guild.get_channel(config.CATEGORY_ID)
        channel = await category.create_text_channel(name=f'ticket-{interaction.author.id}')
        await channel.send(f"Bienvenue dans votre ticket, {interaction.author.mention} !")
        
        button = Button(style=ButtonStyle.red, label="Fermer le ticket", custom_id="close_ticket")
        embed = disnake.Embed(title="Ticket", description="Ceci est un ticket.")
        await channel.send(embed=embed, components=[[button]])

    elif interaction.component.custom_id == "close_ticket":
        await interaction.channel.delete()

bot.run(config.TOKEN)