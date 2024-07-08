import discord
from discord.ext import commands
import requests
import json
from PIL import Image
from io import BytesIO

# Create an instance of Bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

# Command to fetch Roblox user information
@bot.command()
async def roblox(ctx, username):
    await ctx.send(f'Fetching information for {username}...')

    user_info = get_roblox_user_info(username)
    if user_info:
        await ctx.send(f"User ID: {user_info['id']}\nUsername: {user_info['name']}\nDisplay Name: {user_info['displayName']}\nDescription: {user_info['description']}")
    else:
        await ctx.send('User not found.')

def get_roblox_user_info(username):
    url = f'https://users.roblox.com/v1/users/search?keyword={username}&limit=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]
    return None

# Command to fetch detailed Roblox user profile and collection items
@bot.command()
async def rouser(ctx, username):
    users_json = requests.get(f"https://www.roblox.com/search/users/results?keyword={username}&maxRows=1&startIndex=0")
    users = json.loads(users_json.text)
    if not users['UserSearchResults']:
        await ctx.send("User not found.")
        return
    
    user_id = users['UserSearchResults'][0]['UserId']

    profile_json = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
    profile = json.loads(profile_json.text)
    display_name = profile["displayName"]
    created_date = profile["created"]
    description = profile["description"]

    thumbnail_json = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=100x100&format=Png&isCircular=false")
    thumbnail = json.loads(thumbnail_json.text)
    thumbnail_url = thumbnail['data'][0]['imageUrl']

    collections_json = requests.get(f"https://www.roblox.com/users/profile/robloxcollections-json?userId={user_id}")
    collections = json.loads(collections_json.text)
    collection_items = collections["CollectionsItems"]

    embed = discord.Embed(title=f"{username}", url=f"https://www.roblox.com/users/{user_id}/profile", color=0x00b3ff)
    embed.set_author(name="RoUser")
    embed.set_footer(text="Made by AllysonStudiosDev")

    embed.add_field(name="ID", value=f"{user_id}", inline=False)
    embed.add_field(name="Display Name", value=f"{display_name}", inline=True)
    embed.add_field(name="Created", value=f"{created_date}", inline=False)
    embed.add_field(name="Description", value=f"{description}", inline=True)
    embed.set_thumbnail(url=f"{thumbnail_url}")

    # Create a composite image using Pillow
    images = []
    for item in collection_items:
        response = requests.get(item["Thumbnail"]["Url"])
        img = Image.open(BytesIO(response.content))
        images.append(img)

    # Create a blank image for the composite
    composite_width = 140 * len(images)
    composite_height = 140
    composite_image = Image.new("RGBA", (composite_width, composite_height))

    # Paste each image into the composite image
    x_offset = 0
    for img in images:
        composite_image.paste(img, (x_offset, 0))
        x_offset += 140

    # Save the composite image to a BytesIO object
    composite_bytes = BytesIO()
    composite_image.save(composite_bytes, format='PNG')
    composite_bytes.seek(0)

    # Send the composite image as a file and add to embed
    file = discord.File(composite_bytes, filename="composite.png")
    embed.set_image(url="attachment://composite.png")

    await ctx.send(embed=embed, file=file)

# Run the bot with your token
bot.run('TOKEN')
