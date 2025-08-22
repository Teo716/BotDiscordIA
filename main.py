import os
import discord
from discord.ext import commands
from funciones import IARecon, covertirInt
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='%', intents=intents)

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def imagen(ctx, IA = None):
    class_name = ""
    confidence_score = 0.0
    IAs = os.listdir("IAs")
    IA = covertirInt(IA)
    if IA is None or IA < 0 or IA > len(IAs):
        await ctx.send("Por favor, proporciona un número válido para la IA.")
        return
    
    if not ctx.message.attachments:
        await ctx.send("Por favor, adjunta una imagen.")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send("Por favor, adjunta una imagen válida (PNG, JPG, JPEG).")
        return
        
    image_path = f"temp_{attachment.filename}"
    await attachment.save(image_path)
    
    class_name, confidence_score = IARecon(image_path, IAs[IA-1])
    os.remove(image_path)
    await ctx.send(f"La IA {IAs[IA-1]} está {confidence_score}% de que sea un {class_name}")
load_dotenv()
bot.run(os.getenv('TOKEN'))