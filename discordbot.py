from discord.ext import commands
from os import getenv
import traceback
import discord
from discord.channel import VoiceChannel

voiceChannel: VoiceChannel
    
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@client.event
async def on_message(message):
    global voiceChannel

    if message.author.bot:
        return
    if message.content == '!connect':
        voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
        await message.channel.send('ゆずよみが参加しました')
    
@client.event
async def on_message(message):
    global voiceChannel

    if message.author.bot:
        return
   if message.content == '!disconnect':
        voiceChannel.stop()
        await message.channel.send('ゆずよみが退出しました')
        await voiceChannel.disconnect()   
    
    

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
