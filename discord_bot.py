import time
import random as rand
import os
import threading as thread
import subprocess
import discord
import asyncio
import json

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

    async def async_cleanup(self):
        pass
        # TODO: Implement panic script to kill all popups
        # os.startfile(working_dir + 'panic.pyw')
    
    async def close(self):
        # do cleanup here
        await self.async_cleanup()
        await super().close()  # don't forget this!

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    pass

# TODO: Make a default config function when more configs are needed
if not os.path.exists("config.json"):
    with open("config.json", 'w') as f:
        f.write("{\n\t\"discord_token\": \"\"\n}")

with open("config.json", 'r') as f:
    config = json.load(f)

if config["discord_token"] == "":
    print("No discord_token defined in config.json!\nExiting...")
    exit(1)

client.run(config["discord_token"])