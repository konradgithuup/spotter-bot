import logging
import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='%')
# create environment variable for your bot token
BOT_TOKEN = os.environ["BOT_TOKEN_VAR"]
# create environment var for the channel set to be observed
DESIRED_CHANNEL = os.environ["CHANNEL_VAR"]


# get the user's spotting score from the db
def db_lookup(id):
    # TODO: get the spotter's spotting score, probably from a db
    spotting_total = 2
    return spotting_total


# update the user's spotting score after scoring
def db_update(new_total):
    # TODO: update the spotter's spotting score accordingly
    return


@bot.event
async def on_ready():
    logging.info("bot ready")


# command to change the observed channel
# the command may only be used by server members of higher status
@bot.command(brief="<desired channel id>", description="changes the observed channel.\n"
                                                        "The channel id must be passed.\n"
                                                        "Only members with the permission to edit "
                                                        "channels may use this command.")
@commands.has_permissions(manage_channels=True)
async def change_channel(ctx, new_channel_id):
    os.environ["CHANNEL_VAR"] = str(new_channel_id)
    response = f"{ctx.author.name} changed channel to {new_channel_id}"
    logging.info(response)
    await ctx.send(response)


# checks a channel for tags
@bot.event
async def on_message(msg):
    # link message to bot commands
    await bot.process_commands(msg)
    # check whether the message was sent in the channel set to be observed
    print(str(msg.channel))
    if not str(msg.channel.id) == DESIRED_CHANNEL:
        return

    if msg.mentions:
        # format all users mentioned
        tags = ""
        for user in msg.mentions:
            tags += f"{user.name}, "
        tags = tags[:-2]

        # get the spotter stats
        total_tags = db_lookup(msg.author.id)

        # create bot response
        response_form = discord.Embed(
            title="Spotted",
            colour=discord.Colour.green(),
            description=f"""
                        {msg.author.name} spotted {tags}.\n
                        They spotted {total_tags} people in total.
                        """
        )

        # update spotter stats
        db_update(total_tags+len(msg.mentions))

        await msg.channel.send(embed=response_form)

# starts the bot
bot.run(BOT_TOKEN)
