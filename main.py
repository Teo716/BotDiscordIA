import os
import discord
from discord.ext import commands
from funciones import IA

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='%', intents=intents)

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def imagen(ctx):
    if not ctx.message.attachments:
        await ctx.send("Por favor, adjunta una imagen.")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send("Por favor, adjunta una imagen válida (PNG, JPG, JPEG).")
        return
        
    image_path = f"temp_{attachment.filename}"
    await attachment.save(image_path)
    class_name, confidence_score = IA(image_path)
    os.remove(image_path)
    await ctx.send(f"{confidence_score}% de que sea un {class_name}")

bot.run(os.getenv('TOKEN'))