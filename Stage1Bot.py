
import discord
from discord.ext import commands
import pyrebase
import re

# Firebase configuration


firebase = pyrebase.initialize_app(config)
db = firebase.database()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='MeetUp ', intents=intents)

# Regular expression pattern to extract latitude and longitude from Google Maps URL
COORDINATE_PATTERN = r'@(-?\d+\.\d+),(-?\d+\.\d+),\d+z'


def extract_lat_lon_from_google_maps_url(google_maps_url):
    match = re.search(COORDINATE_PATTERN, google_maps_url)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return lat, lon
    else:
        return None, None


# Function to add user coordinates to the MySQL database
def add_coordinates_to_database(user_id, lat, lon):
    connection = aiomysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE)
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_coordinates (user_id, latitude, longitude) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (user_id, lat, lon))
    connection.commit()
    connection.close()

# Function to remove user coordinates from the MySQL database
def remove_coordinates_from_database(user_id):
    connection = aiomysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
    cursor = connection.cursor()
    delete_query = "DELETE FROM user_coordinates WHERE user_id = %s"
    cursor.execute(delete_query, (user_id,))
    connection.commit()
    connection.close()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command()
async def hello(ctx):
    await ctx.send('Hello! Lets MeetUp!')


@client.command()
async def getcord(ctx,link):
    lat, lon = extract_lat_lon_from_google_maps_url(link)
    if lat is not None and lon is not None:
        await ctx.send(f'Coordinates: Latitude: {lat}, Longitude: {lon}')
    else:
        await ctx.send('Invalid Google Maps URL. Please provide a valid link.')



@client.command() #Firebase add
async def add_coords(ctx, google_maps_url):
    lat, lon = extract_lat_lon_from_google_maps_url(google_maps_url)
    if lat is not None and lon is not None:
        # Store coordinates in Firebase
        data = {
            "latitude": lat,
            "longitude": lon
        }
        db.child("user_coordinates").child(str(ctx.author.id)).set(data)
        await ctx.send(f'Coordinates added: Latitude: {lat}, Longitude: {lon}')
    else:
        await ctx.send('Invalid Google Maps URL. Please provide a valid link.')


'''
@client.command()
async def add_coords(ctx,google_maps_url):
    lat, lon = extract_lat_lon_from_google_maps_url(google_maps_url)
    if lat is not None and lon is not None:
        add_coordinates_to_database(ctx.author.id, lat, lon)
        await ctx.send(f'Coordinates added: Latitude: {lat}, Longitude: {lon}')
    else:
        await ctx.send('Invalid Google Maps URL. Please provide a valid link.')

@client.command()
async def remove_coords(ctx):
    remove_coordinates_from_database(ctx.author.id)
    await ctx.send('Coordinates removed successfully.')

'''


client.run('token')

