import disnake
from disnake.ext import commands
from disnake import ButtonStyle, Button

bot = commands.Bot(command_prefix='!')

tickets = []

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def createticket(ctx):
    button = Button(style=ButtonStyle.green, label="Créer un ticket", custom_id="create_ticket")
    embed = disnake.Embed(title="Panel de création de ticket", description="Cliquez sur le bouton ci-dessous pour créer un ticket.")
    message = await ctx.send(embed=embed, components=[button])

    tickets.append(message.id)

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "create_ticket":
        message = await interaction.channel.fetch_message(interaction.message.id)
        category = interaction.guild.get_channel(CATEGORY_ID)
        channel = await category.create_text_channel(name=f'ticket-{interaction.author.id}')
        await channel.send(f"Ticket créé par {interaction.author.mention}")
        await message.edit(embed=None, content="Ticket créé avec succès!", components=[])

@bot.command()
async def closeticket(ctx):
    if isinstance(ctx.channel, disnake.TextChannel) and ctx.channel.category_id == CATEGORY_ID:
        await ctx.channel.delete()
    else:
        await ctx.send('Cette commande doit être utilisée dans un ticket.')

bot.run('YOUR_BOT_TOKEN')