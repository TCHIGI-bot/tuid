import discord
from discord.ext import commands
import os
import threading
import http.server
import socketserver

# تفعيل النوايا المطلوبة للبوت
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# خادم ويب صغير باش يخلّي Koyeb يشوف البوت شغال (على بورت 8080)
def keep_alive():
    PORT = 8080
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
