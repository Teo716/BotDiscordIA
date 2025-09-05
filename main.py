import os
import discord
from discord.ext import commands
from External_IAs import llamada_gemini, llamada_deepseek
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

@bot.command()
async def gemini(ctx, prompt = "quiero que me respondas con este mensaje: 'para la proxima vez no me hagas perder el tiempo'", id = "default_conversation"):
    print(prompt)
    response = llamada_gemini(prompt,id,str(ctx.guild.id),str(ctx.author.id))
    await ctx.send(response)

#@bot.command()
#async def deepseek(ctx, prompt = "quiero que me respondas con este mensaje: 'para la proxima vez no me hagas perder el tiempo'"):
#    print(prompt)
#    response = llamada_deepseek(prompt)
#    await ctx.send(response)

@bot.command()
async def ayuda(ctx):
    ayuda_text = f"""
    Comandos disponibles:
    %imagen [número de IA]: Analiza una imagen adjunta usando la IA seleccionada. Ejemplo: %imagen 1
    %gemini [prompt]: Responde a tu prompt usando el modelo Gemini. Aclaración, el promt se pone entre comillas. Ejemplo: '%gemini \"¿Cuál es la capital de Francia?\"'
    %deepseek [prompt]: Responde a tu prompt usando el modelo DeepSeek. Aclaración, el promt se pone entre comillas. Ejemplo: '%deepseek \"¿Cuál es la capital de Francia?\"'
    %ayuda: Muestra este mensaje de ayuda.
    """
    await ctx.send(ayuda_text)

load_dotenv()
bot.run(os.getenv('TOKEN'))