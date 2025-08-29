import google.generativeai as genai
import os
from openai import OpenAI
from dotenv import load_dotenv

def llamada_gemini(prompt):
    load_dotenv()
    genai.configure(api_key=os.getenv('GEMINI'))
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def llamada_deepseek(prompt):
    client = OpenAI(
    api_key=os.getenv('DEEPSEEK'),
    base_url="https://api.deepseek.com/v1"
    )
    messages = [
    {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
    model="deepseek-chat",  
    messages=messages
    )
    return response.choices[0].message.content