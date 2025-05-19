import discord
from discord.ext import commands
import os
import threading
import http.server
import socketserver

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

def keep_alive():
    PORT = 8080
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
