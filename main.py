import discord
from discord.ext import commands
from discord import app_commands
import os
import threading
import http.server
import socketserver

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- KEEP ALIVE ----
def keep_alive():
    PORT = 8080
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

keep_alive()

# ---- SYNC SLASH COMMANDS ----
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# ---- GENERAL SLASH COMMANDS ----
@bot.tree.command(name="ping", description="اختبار اتصال البوت")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="help", description="عرض قائمة الأوامر")
async def help_cmd(interaction: discord.Interaction):
    help_text = """
**أوامر متاحة:**

/ping — اختبار البوت  
/help — قائمة الأوامر  
/serverinfo — معلومات السيرفر  
/userinfo [member] — معلومات عن عضو  
/avatar [member] — صورة عضو  
/ip — IP سيرفر SAMP  
/discord — رابط ديسكورد السيرفر  
/rules — قوانين السيرفر  
/admins — طاقم الإدارة  
/clear [amount] — مسح رسائل (للأدمن)  
/kick [member] [reason] — طرد عضو (للأدمن)  
/ban [member] [reason] — باند عضو (للأدمن)

/id [player_name] — معرفة ID لاعب  
/joblist — قائمة الوظائف  
/faction [faction_name] — معلومات الفصيل  
/carhelp — أوامر السيارات  
/rphelp — نصائح Roleplay
"""
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.tree.command(name="serverinfo", description="معلومات عن السيرفر")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="معلومات السيرفر", color=discord.Color.blue())
    embed.add_field(name="الاسم", value=guild.name, inline=False)
    embed.add_field(name="عدد الأعضاء", value=guild.member_count, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="معلومات عن عضو")
@app_commands.describe(member="اختر العضو")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title="معلومات العضو", color=discord.Color.green())
    embed.add_field(name="الاسم", value=str(member), inline=True)
    embed.add_field(name="الآيدي", value=member.id, inline=True)
    embed.add_field(name="التحق من", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="عرض صورة عضو")
@app_commands.describe(member="اختر العضو")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(member.avatar.url)

@bot.tree.command(name="ip", description="IP سيرفر SAMP")
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message("IP سيرفر SAMP هو: `play.tunisiacity-rp.com:7777`")

@bot.tree.command(name="discord", description="رابط ديسكورد السيرفر")
async def discord_link(interaction: discord.Interaction):
    await interaction.response.send_message("رابط الدعوة للسيرفر: https://discord.gg/XXXXXXX")

@bot.tree.command(name="rules", description="قوانين السيرفر")
async def rules(interaction: discord.Interaction):
    rules_text = """
**قوانين السيرفر:**
1. إحترام الجميع  
2. لا للسب أو العنصرية  
3. إحترام طاقم الإدارة  
4. لا تنشر روابط بدون إذن  
5. ممنوع السبام أو الإزعاج
"""
    await interaction.response.send_message(rules_text)

@bot.tree.command(name="admins", description="طاقم الإدارة")
async def admins(interaction: discord.Interaction):
    await interaction.response.send_message("**طاقم الإدارة:**\n- Owner: @YourName\n- Admin: @AdminName\n- Support: @SupportRole")

# ---- ADMIN SLASH COMMANDS ----
@bot.tree.command(name="clear", description="مسح عدد من الرسائل (للأدمن فقط)")
@app_commands.describe(amount="عدد الرسائل للمسح")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("ما عندكش صلاحية لمسح الرسائل!", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"تم مسح {len(deleted)} رسالة.", ephemeral=True)

@bot.tree.command(name="kick", description="طرد عضو (للأدمن فقط)")
@app_commands.describe(member="اختر العضو", reason="سبب الطرد")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("ما عندكش صلاحية الطرد!", ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member} تم طرده من السيرفر.")

@bot.tree.command(name="ban", description="باند عضو (للأدمن فقط)")
@app_commands.describe(member="اختر العضو", reason="سبب الباند")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("ما عندكش صلاحية الباند!", ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member} تم عمل باند له من السيرفر.")

# ---- ROLEPLAY SLASH COMMANDS ----

@bot.tree.command(name="id", description="تعرّف على ID لاعب في السيرفر")
@app_commands.describe(player_name="اسم اللاعب")
async def id_cmd(interaction: discord.Interaction, player_name: str):
    # مثال بسيط، تعويض بقاعدة بيانات حقيقية لو عندك
    await interaction.response.send_message(f"ID اللاعب '{player_name}' هو: 12345")

@bot.tree.command(name="joblist", description="عرض قائمة الوظائف المتاحة")
async def joblist(interaction: discord.Interaction):
    jobs = [
        "شرطي", "طبيب", "سائق شاحنة", "ميكانيكي", "تاجر أسلحة", "مسؤول محطة بنزين"
    ]
    await interaction.response.send_message("قائمة الوظائف المتاحة:\n- " + "\n- ".join(jobs))

@bot.tree.command(name="faction", description="معلومات عن فصيلتك")
@app_commands.describe(faction_name="اسم الفصيل")
async def faction(interaction: discord.Interaction, faction_name: str):
    # مثال ثابت، عوّض بالمعلومات الحقيقية
    await interaction.response.send_message(f"معلومات عن الفصيل '{faction_name}':\n- عدد الأعضاء: 25\n- رتبة أعلى: قائد")

@bot.tree.command(name="carhelp", description="أوامر السيارات داخل السيرفر")
async def carhelp(interaction: discord.Interaction):
    text = """
أوامر السيارات في سيرفر RP:
- /carspawn [اسم السيارة] — استدعاء سيارة  
- /carfix — تصليح السيارة  
- /carlock — قفل/فتح السيارة  
- /carflip — قلب السيارة إذا انقلبت
"""
    await interaction.response.send_message(text)

@bot.tree.command(name="rphelp", description="نصائح للعب Roleplay")
async def rphelp(interaction: discord.Interaction):
    tips = """
نصائح للعب Roleplay:
- إحترم القصة والشخصية متاعك  
- لا تتصرف خارج إطار الدور  
- استعمل الدردشة الخاصة بـ RP فقط  
- احترم تعليمات الإدارة
"""
    await interaction.response.send_message(tips)

# ---- RUN BOT ----
bot.run(os.getenv("DISCORD_TOKEN"))
