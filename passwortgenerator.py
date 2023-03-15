import discord
import random
import string

client = discord.Client()

@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):
    if message.content == '!passwort':
        # Password Gen
        password_length = 20
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_characters) for i in range(password_length))

        # Antwort senden
        await message.channel.send(f'New Password: {password}')

# Discord Bot Token einsetzen
client.run('TOKEN')
