# Discord bot

from dotenv import load_dotenv
import os
import random
import asyncio
import discord


load_dotenv()

BOT_PREFIX = "!"
TOKEN = os.getenv("SECRET_TOKEN")  # Get at discordapp.com/developers/applications/me


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(BOT_PREFIX + "help"):
        await message.channel.send(
            "====DocketBot Commands====\n\n"
            + "'!help' Lists all the DocketBot commands.\n"
            + "'!add *movie*' Adds the movie to the docket.\n"
            + "'!remove *movie*' Removes the movie from the docket.\n"
            + "'!docket' Lists entire docket.\n"
            + "'!pick' Chooses a random movie from the docket.\n"
        )

    # add a movie to the docket
    elif message.content.startswith(BOT_PREFIX + "add"):
        movie = message.content.split(" ", maxsplit=1)[1].title()
        docketAdd(movie)
        await message.channel.send(movie + " added to the docket.")

    # remove a movie to the docket
    elif message.content.startswith(BOT_PREFIX + "remove"):
        movie = message.content.split(" ", maxsplit=1)[1].title()
        docketRemove(movie)
        await message.channel.send(movie + " removed from the docket.")

    # list all movies in the docket
    elif message.content.startswith(BOT_PREFIX + "docket"):
        await message.channel.send(docketPrint())

    # picks a random movie in the docket
    elif message.content.startswith(BOT_PREFIX + "pick"):
        await message.channel.send(docketRandom())


# ====COMMAND FUNCTIONS====
def docketAdd(movie):
    with open("docket.txt", "a") as docket:
        docket.write(movie + "\n")


def docketRemove(movie):
    with open("docket.txt") as docket:
        lines = docket.readlines()

    with open("docket.txt", "w") as docket:
        for line in lines:
            if line.strip("\n") != movie:
                docket.write(line)


def docketPrint():
    with open("docket.txt") as docket:
        response = docket.read()
        if response == "":
            response = "The docket is empty."
        return response


def docketRandom():
    with open("docket.txt") as docket:
        movies = docket.read().splitlines()
        pick = "Did not find any movies to pick from."
        if len(movies) > 0:
            pick = random.choice(movies)
        return pick


client.run(TOKEN)
