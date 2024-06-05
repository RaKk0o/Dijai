import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Bot init
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Spotify conf
spotify_client_id = 'VOTRE_SPOTIFY_CLIENT_ID'
spotify_client_secret = 'VOTRE_SPOTIFY_CLIENT_SECRET'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id,
                                                           client_secret=spotify_client_secret))

# Join Voice
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Vous devez être dans un salon vocal pour utiliser cette commande.")

# Left Voice
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Je ne suis pas connecté à un salon vocal.")

# Play Music from a link
@bot.command()
async def play(ctx, url: str):
    async def play_song(ctx, song_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')

            ctx.voice_client.play(source, after=lambda e: print(f'Erreur: {e}') if e else None)

    if 'spotify.com' in url:
        results = sp.track(url)
        track_name = results['name']
        artist_name = results['artists'][0]['name']
        query = f'{track_name} {artist_name} lyrics'
        results = sp.search(q=query, limit=1)
        track = results['tracks']['items'][0]
        youtube_url = f"https://www.youtube.com/watch?v={track['id']}"
        await play_song(ctx, youtube_url)
    else:
        await play_song(ctx, url)

# Start bot
bot.run('VOTRE_TOKEN_DISCORD')
