import discord
from parse_and_store import store_problem_set

client = discord.Client()
with open('token.txt', 'r') as reader:
    token = reader.read()

amc = y1 = y2 = p1 = p2 = None


@client.event
async def on_ready():
    print(f'{client.user} is ready!')


@client.event
async def on_message(message):
    global amc, y1, y2, p1, p2
    if message.author == client.user:
        return

    if message.content.lower().startswith('$hey'):
        await message.channel.send(
            "Hey! I am AoPS Bot. Do you need a problem set? \nWhich AMC are you intersted in? \nType: amc 8 (or amc 10a, ..., amc 12b)")

    if message.content.lower() in ("amc 8", "amc 10a", "amc 10b", "amc 12a", "amc 12b"):
        amc = message.content.split()[1]
        await message.channel.send(
            'Great. What period of are you interested in?\n(min: 1999, max:2020)\nExample: year 2007 2013')

    if message.content.lower().startswith('year') and message.content.count(' ') == 2:
        if message.content.split()[1].isnumeric() and message.content.split()[2].isnumeric():
            if int(message.content.split()[1]) in range(2000, 2021) and int(message.content.split()[2]) in range(2000,
                                                                                                                 2021):
                y1 = int(message.content.split()[1])
                y2 = int(message.content.split()[2])
                await message.channel.send('Now. Problem numbers range?\n(min: 1, max: 25)\nExample: range 3 21')

    if message.content.lower().startswith('range') and message.content.count(' ') == 2:
        if message.content.split()[1].isnumeric() and message.content.split()[2].isnumeric():
            if int(message.content.split()[1]) in range(1, 26) and int(message.content.split()[2]) in range(1, 26):
                p1 = int(message.content.split()[1])
                p2 = int(message.content.split()[2])
                await message.channel.send("Type 'gen' to generate the problem set")

    if message.content.lower() == "gen":
        file_names = store_problem_set(amc="8", y1=2018, y2=2020, p1=3, p2=5)
        my_files = [discord.File(name) for name in file_names]
        await message.channel.send(files=my_files)


client.run(token)
