import discord
import datetime
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot('!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity = discord.Activity(
        type = discord.ActivityType.watching,

        #Bot status
        name = f'{members} members' 

    ))
    print('Ready to support ✅')

#Ticket command
@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    await ctx.message.delete()

    #Embed title and description
    embed = discord.Embed(title ='Tickets', description ='Welcome to tickets system.', color=config.embed_color) 

    #Embed image
    embed.set_image(url='https://i.imgur.com/FoI5ITb.png')

    await ctx.send(
        embed = embed,

        #Embed button
        components = [
            Button(
                custom_id = 'Ticket',
                label = "Create a ticket",
                style = ButtonStyle.green,
                emoji ='🔧')
        ]
    )

@bot.event
async def on_button_click(interaction):

    canal = interaction.channel
    canal_logs = interaction.guild.get_channel(config.id_channel_ticket_logs)

    #Select function
    if interaction.component.custom_id == "Ticket":
        await interaction.send(

            components = [
                Select(
                    placeholder = "How can we help you?",
                    options = [
                        SelectOption(label="Question", value="question", description='If you have a simple question.', emoji='❔'),
                        SelectOption(label="Help", value="help", description='If you need help from us.', emoji='🔧'),
                        SelectOption(label="Report", value="report", description='To report a misbehaving user.', emoji='🚫'),
                    ],
                    custom_id = "menu")])

    #Call staff function
    elif interaction.component.custom_id == 'call_staff':

        embed_llamar_staff = discord.Embed(description=f"🔔 {interaction.author.mention} has called the staff.", color=config.embed_color)
        await canal.send(f'<@&{config.id_staff_role}>', embed=embed_llamar_staff, delete_after= 20)

    #Close ticket function
    elif interaction.component.custom_id == 'close_ticket':

        embed_cerrar_ticket = discord.Embed(description=f"⚠️ Are you sure you want to close the ticket?", color=config.embed_color)
        await canal.send(interaction.author.mention, embed=embed_cerrar_ticket, 
                        components = [[
                        Button(custom_id = 'close_yes', label = "Yes", style = ButtonStyle.green),
                        Button(custom_id = 'close_no', label = "No", style = ButtonStyle.red)]])

    #Ticket logs function
    elif interaction.component.custom_id == 'close_yes':

        await canal.delete()
        embed_logs = discord.Embed(title="Tickets", description=f"", timestamp = datetime.datetime.utcnow(), color=config.embed_color)
        embed_logs.add_field(name="Ticket", value=f"{canal.name}", inline=True)
        embed_logs.add_field(name="Closed by", value=f"{interaction.author.mention}", inline=False)
        embed_logs.set_thumbnail(url=interaction.author.avatar_url)
        await canal_logs.send(embed=embed_logs)


    elif interaction.component.custom_id == 'close_no':
        await interaction.message.delete()

@bot.event
async def on_select_option(interaction):
    if interaction.component.custom_id == "menu":

        guild = interaction.guild
        category = discord.utils.get(interaction.guild.categories, id = config.id_category)
        rol_staff = discord.utils.get(interaction.guild.roles, id = config.id_staff_role)

        #Select option | Question
        if interaction.values[0] == 'question':

            #Creating ticket channel | Question
            channel = await guild.create_text_channel(name=f'❔┃{interaction.author.name}-ticket', category=category)
            
            #Ticket channel permissions | Question
            await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                            send_messages=False,
                            read_messages=False)
            await channel.set_permissions(interaction.author, 
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True)
            await channel.set_permissions(rol_staff,
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True,
                                                manage_messages=True)
                                                

            await interaction.send(f'> The {channel.mention} channel was created to solve your questions.', delete_after= 3)

            #Inside the ticket | Question
            #Embed inside the ticket | Question
            embed_question = discord.Embed(title=f'Question - ¡Hi {interaction.author.name}!', description='In this ticket we have an answer to your question.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`..', color=config.embed_color)
            embed_question.set_thumbnail(url=interaction.author.avatar_url)


            await channel.send(interaction.author.mention, embed=embed_question,
            
            #Embed buttons inside the ticket | Question
             components = [[
                    Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                    Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])


        #Select option | Help
        elif interaction.values[0] == 'help':

            #Creating ticket channel | Help
            channel = await guild.create_text_channel(name=f'🔧┃{interaction.author.name}-ticket', category=category)
            
            #Ticket channel permissions | Help
            await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                            send_messages=False,
                            read_messages=False)
            await channel.set_permissions(interaction.author, 
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True)
            await channel.set_permissions(rol_staff,
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True,
                                                manage_messages=True)


            await interaction.send(f'> The {channel.mention} channel was created to help you.', delete_after= 3)

            #Inside the ticket | Help
            #Embed inside the ticket | Help
            embed_question = discord.Embed(title=f'Help - ¡Hi {interaction.author.name}!', description='In this ticket we can help you with whatever you need.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`.', color=config.embed_color)
            embed_question.set_thumbnail(url=interaction.author.avatar_url)


            await channel.send(interaction.author.mention, embed=embed_question, 
            
            #Embed buttons inside the ticket | Help
            components = [[
                    Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                    Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])


        #Select option | Report
        elif interaction.values[0] == 'report':

            #Creating ticket channel | Report
            channel = await guild.create_text_channel(name=f'🚫┃{interaction.author.name}-ticket', category=category)

            #Ticket channel permissions | Report
            await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                            send_messages=False,
                            read_messages=False)
            await channel.set_permissions(interaction.author, 
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True)
            await channel.set_permissions(rol_staff,
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                attach_files=True,
                                                read_message_history=True,
                                                external_emojis=True,
                                                manage_messages=True)


            await interaction.send(f'> The {channel.mention} channel was created to report to the user.', delete_after= 3)

            #Inside the ticket | Report
            #Embed inside the ticket | Report
            embed_question = discord.Embed(title=f'Report - ¡Hi {interaction.author.name}!', description='In this ticket we can help you with your report.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`.', color=config.embed_color)
            embed_question.set_thumbnail(url=interaction.author.avatar_url)

            await channel.send(interaction.author.mention, embed=embed_question, 
            
            #Embed buttons inside the ticket | Report
            components = [[
                    Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                    Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])

bot.run(config.TOKEN)