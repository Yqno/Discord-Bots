import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
voice_client = None

@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, *, url):
    global voice_client
    
    # connect to voice channel
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel.")
        return
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()
    
    # download the audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        song = info['title'] + '.mp3'
    
    # play the audio
    voice_client.play(discord.FFmpegPCMAudio(song))
    await ctx.send(f"Playing: {song}")

@bot.command(name='stop', help='Stops the current song and clears the queue')
async def stop(ctx):
    global voice_client
    
    # stop playing audio
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Stopped playing.")

@bot.command(name='resume', help='Resumes the current song')
async def resume(ctx):
    global voice_client
    
    # resume playing audio
    if voice_client and not voice_client.is_playing():
        voice_client.resume()
        await ctx.send("Resumed playing.")

@bot.command(name='disconnect', help='Disconnects the bot from the voice channel')
async def disconnect(ctx):
    global voice_client
    
    # disconnect from voice channel
    if voice_client:
        await voice_client.disconnect()
        voice_client = None
        await ctx.send("Disconnected from voice channel.")

@bot.command(name='start', help='Starts the bot and connects to a voice channel')
async def start(ctx):
    global voice_client
    
    # connect to voice channel
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel.")
        return
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()
    await ctx.send(f"Connected to voice channel: {voice_client.channel}")



@bot.command()
async def skip(ctx):
    voice_client = ctx.guild.voice_client

    if not voice_client:
        return await ctx.send("Not connected to a voice channel.")

    if not voice_client.is_playing():
        return await ctx.send("Not playing any music.")

    voice_client.stop()
    await ctx.send("Skipping current song.")


# Fügt einen Befehl hinzu, um einen Invite-Link zu generieren
@bot.command(name='invite')
async def invite_command(ctx):
    await ctx.send(f'Einladungslink: {discord.utils.oauth_url(bot.user.id)}')


# start the bot
bot.run('Your Token Here')
