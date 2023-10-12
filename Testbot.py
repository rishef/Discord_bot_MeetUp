import discord
from discord.ext import commands
import googlemaps

intents = discord.Intents.all()
client = commands.Bot(command_prefix = 'MeetUp ', intents = intents)

# Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command()
async def hello(ctx):
    await ctx.send('Hello! Lets MeetUp!')


@client.command()
async def nearby_restaurants(ctx, *, location):
    try:
        # Geocode the provided location using Google Maps API
        geocode_result = gmaps.geocode(location)

        if not geocode_result:
            await ctx.send(f'Could not find the location: {location}')
            return

        # Extract latitude and longitude from the geocode result
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        # Perform a nearby search for restaurants using Google Maps Places API
        places_result = gmaps.places_nearby(location=(lat, lng), radius=1000, type='restaurant')

        # Extract restaurant names from the API response
        restaurant_names = [place['name'] for place in places_result['results']]

        if restaurant_names:
            await ctx.send(f'Nearby restaurants in {location}: \n{", ".join(restaurant_names)}')
        else:
            await ctx.send(f'No restaurants found near {location}')

    except Exception as e:
        print(str(e))
        await ctx.send('An error occurred while processing your request.')

client.run('Token')
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run('YOUR_DISCORD_BOT_TOKEN')
'''