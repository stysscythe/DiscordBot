import discord
from discord.ext import commands

TOKEN = 'WsM20N76CGOQZwltGGdie2FNM7LeygK0'

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

# Specify the user ID allowed to use the restricted commands
allowed_user_id = "1125548649175322654"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def send_webhook(channel, message):
    webhook = await channel.create_webhook(name="Bot Webhook")
    await webhook.send(message)

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if str(ctx.author.id) != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    await member.ban(reason=reason)
    await send_webhook(ctx.channel, f'{member.mention} has been banned.')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if str(ctx.author.id) != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    await member.kick(reason=reason)
    await send_webhook(ctx.channel, f'{member.mention} has been kicked.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    if str(ctx.author.id) != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    await ctx.channel.purge(limit=limit + 1)
    await send_webhook(ctx.channel, f'{limit} messages have been purged.')

@bot.command()
async def info(ctx, member: discord.Member):
    if str(ctx.author.id) != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    embed = discord.Embed(title=f'{member}', description=f'ID: {member.id}', color=discord.Color.blurple())
    embed.set_thumbnail(url=member.avatar_url)
    await send_webhook(ctx.channel, embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid arguments provided for the command.")
    else:
        await ctx.send("An error occurred while processing the command.")

bot.run(TOKEN)
