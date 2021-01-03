import discord
client = discord.Client()

with open('token.txt','r') as reader:
    token = reader.read()

@client.event
async def on_ready():
    print(f'{client.user} is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(token)