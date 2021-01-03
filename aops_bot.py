import discord
from search_tool import search

client = discord.Client()
with open('token.txt', 'r') as reader:
    token = reader.read()

amcs, years, problems, key_words = None, None, None, None


@client.event
async def on_ready():
    print(f'{client.user} is ready!')


@client.event
async def on_message(message):
    global amcs, years, problems, key_words
    if message.author == client.user:
        return

    if message.content.startswith('Hello'):
        await message.channel.send("A - amc classes \nY - years \nP - problems range \nK - key words \nS - search")

    if message.content.startswith('A') or message.content.startswith('a'):
        amcs = message.content.split()[1:]
        await message.channel.send("Ok...")

    if message.content.startswith('Y') or message.content.startswith('y'):
        years = message.content.split()[1:]
        await message.channel.send("Ok...")

    if message.content.startswith('P') or message.content.startswith('p'):
        problems = message.content.split()[1:]
        await message.channel.send("Ok...")

    if message.content.startswith('K') or message.content.startswith('k'):
        key_words = message.content.split()[1:]
        await message.channel.send("Ok...")

    if message.content.startswith('S') or message.content.startswith('s'):
        if amcs and years:
            results = search(amcs, years, problems, key_words)
            await message.channel.send(results)


client.run(token)
