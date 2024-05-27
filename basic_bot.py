import discord
from discord import app_commands, Embed
# from discord.ext import commands
import random
import requests
import emoji
import dotenv
import os

JACKS_API_URL = "https://api.kodypay.com/web/merchants/59a27b93-14f9-4c48-86ef-aae89be23507/items/b29f6302-a77e-4877-8015-14e141904ae0/addonInfo"
JACKS_ORDER_URL = "https://pay.kodypay.com/store/ae3b2092-0938-4a3d-b1a5-32fa8c6fdfbe/table?table=1"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def get_emoji(item):
    if 'secret' in item.lower():
        return '⭐'
    em = emoji.get_top_emoji(item)
    if em is None:
        return '🍨'
    return em

def get_jacks_menu():
    req = requests.get(JACKS_API_URL)
    req = req.json()
    addon_groups = req['addonGroups']
    flavours = [a for a in addon_groups if a['addonGroupName'] == 'Choose your flavour'][0]['addons']
    flavours = [f['name'].strip() for f in flavours]
    flavours = [f'{get_emoji(f)} {f}' for f in flavours]
    return flavours

adjectives = [
    "Joyful",
    "Jovial",
    "Jubilant",
    "Java-powered",
    "Jazzy",
    "Jocular",
    "Judicious",
    "Juicy",
    "Jumbo",
    "Jaunty",
    "Jolly",
    "Jeweled",
    "Jesting",
    "Jumpy",
    "Jaw-dropping",
    "Jammed",
    "Jubilatory",
    "Jocund",
    "Juvenescent",
    "Jessant",
    "Jargon-free",
]

@tree.command(name = "jacks", description = "Get the Jacks menu")#, guild=discord.Object(id=132521497192300544)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def jacks(interaction):
    # await interaction.response.send_message("Hello!")
    menu = get_jacks_menu()
        # Create a new Embed object
    embed = Embed(title="Jack's Gelato Menu (Realtime)", url=JACKS_ORDER_URL)
    items_str = "\n".join(menu)
    embed.description = items_str
    embed.colour = discord.Colour.dark_gold()
    embed.set_footer(text=f"{random.choice(adjectives)} Jacks Bot (now with AI!)")

    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    await tree.sync()#guild=discord.Object(id=132521497192300544))
    print("Ready!")

dotenv.load_dotenv()
client.run(os.environ["JACKS_DISCORD_TOKEN"])
