import discord
from discord.ext import commands
import os

def main():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = '!', intents = intents)

    @client.event
    async def on_ready():
        print(f"{client.user.name} is online")

    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            client.load_extension(f"modules.{folder}.cog")

    with open('token.txt', 'r') as token:
        client.run(token.read())

if __name__ == '__main__':
    main()