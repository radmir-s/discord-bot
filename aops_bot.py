import discord
from parse_and_store import prepare_zip
from os import remove

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

    if message.content.upper() in ("AMC 8", "AMC 10A", "AMC 10B", "AMC 12A", "AMC 12B"):
        amc = message.content.upper().replace(" ","_")
        await message.channel.send(
            'Great. What period of are you interested in?\n(min: 1999, max:2020)\nExample: year 2007 2013')

    if message.content.lower().startswith('year') and message.content.count(' ') == 2:
        y1, y2 = message.content.split()[1:3]
        if y1.isnumeric() and y2.isnumeric():
            y1 = max(1999, int(y1))
            y2 = min(2020, int(y2))
            await message.channel.send('Now. Problem numbers range?\n(min: 1, max: 25)\nExample: range 3 21')

    if message.content.lower().startswith('range') and message.content.count(' ') == 2:
        p1, p2 = message.content.split()[1:3]
        if p1.isnumeric() and p2.isnumeric():
            p1 = max(1, int(p1))
            p2 = min(25, int(p2))
            await message.channel.send("Type 'gen' to generate the problem set")

    if p1 and amc:
        if p1 < 2003 and amc != "AMC_8":
            p1 = max(2000, p1)
            p2 = max(2000, p2)
            amc = "AMC_10" if amc[5] == "0" else "AMC_12"

    if message.content.lower() == "gen":
        print(amc, y1, y2, p1, p2)
        zip_file_name = prepare_zip(amc, y1, y2, p1, p2)
        await message.channel.send(file=discord.File(zip_file_name))
        remove(zip_file_name)


client.run(token)
