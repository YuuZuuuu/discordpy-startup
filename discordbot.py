from discord.ext import commands
from os import getenv
import traceback
import discord
import html
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
from google.cloud import texttospeech


TOKEN = 'YOUR_TOKEN'
client = discord.Client()


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
async def on_ready():
    print('Login!!!')


@client.event
async def on_message(message):
    global voiceChannel

    if message.author.bot:
        return
    if message.content == '!con':
        voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
        await message.channel.send('ゆずよみが参加しました')
        return
    elif message.content == '!dis':
        voiceChannel.stop()
        await message.channel.send('ゆずよみが退出しました')
        await voiceChannel.disconnect()
        return

    play_voice(message.content)

def text_to_ssml(text):
    escaped_lines = html.escape(text)
    ssml = "{}".format(
        escaped_lines.replace("\n", '\n<break time="1s"/>')
    )
    return ssml

def ssml_to_speech(ssml, file, language_code, gender):
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + file)
    return file

def play_voice(text):
    ssml = text_to_ssml(text)
    file = ssml_to_speech(ssml, "voice.mp3", "ja-JP", texttospeech.SsmlVoiceGender.MALE)
    voiceChannel.play(FFmpegPCMAudio(file))

client.run(TOKEN)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
