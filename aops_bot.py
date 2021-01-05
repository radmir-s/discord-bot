import discord
from search_tool import *

client = discord.Client()
with open('token.txt', 'r') as reader:
    token = reader.read()

amc = years = problems = key_words = None


@client.event
async def on_ready():
    print(f'{client.user} is ready!')


@client.event
async def on_message(message):
    global amc, years, problems, key_words
    if message.author == client.user:
        return

    if message.content.startswith('Hello'):
        await message.channel.send("A - amc classes \nY - years range \nP - problems range \nS - search")

    if message.content.startswith('A') or message.content.startswith('a'):
        amc = message.content.split()[1]
        await message.channel.send("Ok.")

    if message.content.startswith('Y') or message.content.startswith('y'):
        years = message.content.split()
        await message.channel.send("Ok.")

    if message.content.startswith('P') or message.content.startswith('p'):
        problems = message.content.split()
        await message.channel.send("Ok.")

    if message.content.startswith('S') or message.content.startswith('s'):
        if amc and years:
            y1 = int(years[1])
            y2 = int(years[2])
            try:
                p1 = int(problems[1])
                p2 = int(problems[2])
            except:
                p1 = 1
                p2 = 25




client.run(token)
