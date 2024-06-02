import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from discord import Embed
import asyncio
import io
import datetime
import sqlite3
from discord import *
from discord.ext import commands
from discord.ext.commands import has_permissions

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

TOKEN = ''



@bot.command()
async def ticket(ctx):
    embed = discord.Embed(title="Tickets", description="Ti serve aiuto? Nessun problema! Usa la reazione qua sotto per creare un nuovo ticket dove il nostro staff ti assisterà.", color=0x00ff00)

    
    select = Select(placeholder="Scegli una Categoria...",
                    options=[
                        discord.SelectOption(label="Supporto", description="Crea un Supporto Ticket", emoji="🛠"),
                        discord.SelectOption(label="Store", description="Crea un Ticket Store", emoji="💸"),
                        discord.SelectOption(label="Generale", description="Crea Ticket Generale", emoji="❓"),
                        discord.SelectOption(label="Segnalazione Player", description="Segnalare un Player"),
                        discord.SelectOption(label="Lifesteal", description="Ticket per la Lifesteal"),
                        discord.SelectOption(label="Survival", description="Ticket per la Survival"),
                        discord.SelectOption(label="KitPVP", description="Ticket per il KitPVP"),
                        discord.SelectOption(label="BedWars", description="Ticket per Le BedWars"),
                        discord.SelectOption(label="Appeal di Un Ban", description="Per richiedere unBan"),
                    ])
    
    async def select_callback(interaction):
        category = select.values[0]
        channel_name = f"{category.lower()}-ticket"
        guild = interaction.guild

        
        new_channel = await guild.create_text_channel(name=channel_name, category=None)
        
        
        close_embed = discord.Embed(title="Ticket", description="Usa il bottone sotto per chiudere questo ticket.", color=0xff0000)
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.danger)

        async def close_button_callback(interaction):

            await new_channel.delete(reason="Ticket closed")

        close_button.callback = close_button_callback

        
        question_button = Button(label="Ask Questions", style=discord.ButtonStyle.primary)
        second_button = Button(label="Second Button", style=discord.ButtonStyle.primary)

        async def question_button_callback(interaction):
            questions = ["Qual è il problema?", "Da quanto tempo riscontri questo problema?", "Hai provato qualche soluzione?"]
            answers = []

            for question in questions:
                await interaction.response.send_message(question, ephemeral=True)
                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel
                msg = await bot.wait_for('message', check=check)
                answers.append(msg.content)

            
            response_embed = discord.Embed(title="Risposte dell'utente", color=0x00ff00)
            for question, answer in zip(questions, answers):
                response_embed.add_field(name=question, value=answer, inline=False)

            await new_channel.send(embed=response_embed)
            await interaction.followup.send("Le tue risposte sono state registrate.", ephemeral=True)

        question_button.callback = question_button_callback

        
        view = View()
        view.add_item(select)
        view.add_item(question_button)
        view.add_item(second_button)
        view.add_item(close_button)

        await new_channel.send(embed=close_embed, view=view)
        await interaction.response.send_message(f"Creato un nuovo canale: {new_channel.mention}", ephemeral=True)

    select.callback = select_callback

    
    view = View()
    view.add_item(select)

    
    await ctx.send(embed=embed, view=view)







bot.run(TOKEN)
