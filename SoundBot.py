# TODO should probbably add some logging functionality

import os
import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from requests import get

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!!")

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)

def remove(dir):
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))

def list_files():
    list = ["None", "None", "None", "None", "None"]
    for i in range(1, 6):
        for file in os.listdir(str(i)):
            list[i - 1] = file
    return list

@bot.command(name="upload", help="Uploads a sound to the bot")
async def upload(ctx, sound_name, sound_number):
    if len(ctx.message.attachments) == 0:
        await ctx.send("No attachment was included")
    else:
        if int(sound_number) < 1 or int(sound_number) > 5:
            await ctx.send("Sound number not valid")
        else:
            if ".mp3" in ctx.message.attachments[0].url or ".wav" in ctx.message.attachments[0].url:
                remove(sound_number)
                download(ctx.message.attachments[0].url, sound_number + "/" + sound_name)
                await ctx.send("Sound was uploaded")
            else:
                await ctx.send("File was not an MP3 or WAV so it was not uploaded")

@bot.command(name="play", help="Plays a sound")
async def play(ctx, sound_number: int):
    list = list_files()
    if sound_number < 1 or sound_number > 5 or list[sound_number - 1] == "None":
        await ctx.send("Sorry there is no sound associated with that number...Try picking from the list bellow\n")
        msg = "1: " + list[0] + "\n" + "2: " + list[1] + "\n" + "3: " + list[2] + "\n" + "4: " + list[3] + "\n" + "5: " + list[4] + "\n"
        await ctx.send(msg)
    else:
        channel = ctx.author.voice.channel
        audio = FFmpegPCMAudio(str(sound_number) + '/' +  list[sound_number - 1])
        voice_chat = await channel.connect() 
        await ctx.send("Playing " + str(list[sound_number - 1]))
        voice_chat.play(audio)
        while voice_chat.is_playing(): 
            await asyncio.sleep(1)
        await ctx.voice_client.disconnect()

@bot.command(name="list", help="Prints a list of all the sounds that can be played")
async def list(ctx):
    list = list_files()
    msg = "1: " + list[0] + "\n" + "2: " + list[1] + "\n" + "3: " + list[2] + "\n" + "4: " + list[3] + "\n" + "5: " + list[4] + "\n" 
    await ctx.send(msg)

bot.run(TOKEN)
