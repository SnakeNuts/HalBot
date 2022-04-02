import os

from datetime import datetime, timedelta
from discord.ext import commands
from pytz import utc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

# set Scheduler job storgae
jobstores = {'default': MemoryJobStore()}

# set Scheduler executor
executors = {'default': AsyncIOExecutor()}

# create and start Scheduler
scheduler = AsyncIOScheduler(jobstores=jobstores,
                             executors=executors,
                             timezone=utc)
scheduler.start()

# get the Discord bot token
TOKEN = os.environ['DISCORD_TOKEN']

# Initialise the bot
bot = commands.Bot(command_prefix='>')


# Connection logging
@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')


# Outgoing DM sender
async def send_message(recipient):
  await recipient.send("Test every 1 minute")


# so the remind command will be
# ">remind [user] about [subject] in [duration]"
# or
# ">remind [user] about [subject] at [time]"


# React to incoming messages
@bot.command(name='remind')
async def remind(ctx, *words):
  server = ctx.guild
  channel = ctx.channel
  author = ctx.author

  await ctx.send(
    f"The parameters were {' '.join(words)}, {server}, {channel}, {author}")

  interval = datetime.now() + timedelta(seconds=10)
  scheduler.add_job(send_message, 'date', args=[author, ], run_date=interval)
  

# Start the bot.
bot.run(TOKEN)
