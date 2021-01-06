import discord

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
    else:
        await message.channel.send("Hello! I am AoPS Bot.\n I can pull a problem or a problem set for you.\n 1 - problem\n 2 - problem set"




    if message.content.startswith('A') or message.content.startswith('a'):
        await message.channel.send('Ok.')





client.run(token)
