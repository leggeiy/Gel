import discord
from discord.ext import commands
from config import token   # Import the bot's token from configuration file
import random
from facts import factsies
intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Mengabaikan pesan dari bot itu sendiri

    if any(word.startswith('http') for word in message.content.split()):  # Memeriksa apakah pesan berisi tautan
        await message.author.ban(reason="Dilarang mengirim tautan")  # Melarang penulis pesan
        await message.channel.send(f"{message.author.mention} diblokir karena mengirim tautan.")  # Membuat pengumuman dalam obrolan

    await bot.process_commands(message)  # Penting untuk memanggil fungsi ini agar perintah tetap berjalan

@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

@bot.command()
async def start(ctx): # !star
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True) # comman !ban membutuhkan permission, apakah termasuk dalam member atau tidak
async def ban(ctx, member: discord.Member = None): # !ban budi
    if member:
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")
@bot.command()
async def facts(ctx):
    a = random.choice(factsies)
    await ctx.send(a)

bot.run(token)