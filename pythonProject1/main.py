import os
import discord



intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'general':
        ints = predict_class(user_message)
        res = get_response(ints, intents)
        await message.channel.send(res)
        return

client.run('MTEwNjM5MzM1NjYxMjkyNzUwOQ.G9oWgg.dbzttOtD7MILqETrTliWAlbeQF14afGywVan78')


