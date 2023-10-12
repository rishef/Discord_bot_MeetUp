import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = 'MeetUp ', intents = intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command()
async def hello(ctx):
    await ctx.send('Hello! Lets MeetUp!')

client.run('MTE1NzkzMTcxNzgyNzQ5MzkwMA.G4n8ne.3XMJHx7lLud9mnoxCbxzmdpHmD6uB9tWAHi2Xo')
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run('YOUR_DISCORD_BOT_TOKEN')
'''