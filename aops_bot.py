import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run('NzQ3MDgzMTI4NDA4ODk5NjQ2.X0JtYQ.SZfqzA5ztxnYn8sp6MrMN-ZNpQw')