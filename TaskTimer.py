import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from datetime import datetime
import environ

env = environ.Env()
env.read_env('.env')
TOKEN = env('TOKEN')
CHANNEL_ID = int(env('channel'))

bot = Bot(command_prefix="!",intents=discord.Intents.all())
channel = bot.get_partial_messageable(CHANNEL_ID)

weekday_dic = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
task =[]

def validate_input(task_data):
    """
    Check if the input data is valid or not
    """
    try:
        if not task_data[0].strip():
            return False, "Task name can not be empty"
        
        weekday = int(task_data[1])
        if weekday < 0 or weekday > 6:
            return False, "Weekday should be an integer between 0 and 6"
        
        time_str = task_data[2]
        if len(time_str) != 4 or not time_str.isdigit():
            return False, "Time should be in the format HHMM"
        time = datetime.strptime(time_str, "%H%M").time()
        
        return True, ""
    except (IndexError, ValueError):
        return False, "Invalid input format.\n Please use the format: !add_task(task, weekday(monday:0 ... sunday:6), time(1830))"

@tasks.loop(minutes=1)
async def daily_task_checker():

    """
    Notify today's task when the day changes.
    """

    global result,channel

    dt_now = datetime.now()
    now = dt_now.strftime("%H%M")
    weekday_now = dt_now.weekday()
    result = [x for x in task if x[1] == weekday_now]

    if now == "0000":
        print("passed 2")
        if result: 
            await channel.send(f"Remember you need to submit {len(result)} {'ttaasskks'[len(result)==1::2]}! @everyone")
        else: 
            await channel.send("No task today, yay!")

@tasks.loop(minutes=1)
async def task_reminder():

    """
    Notify when time remaining on a task is approaching
    """

    global result,channel

    dt_now = datetime.now()
    now = dt_now.strftime("%H%M")
    
    for r in result:
        if 0 <= (int(r[2]) - int(now)) <= 200:
                print(result)
                await channel.send(f"Remember you need to submit '{r[0]}' within 2 hours! @everyone")
                # result.remove(r)
                print(result)

@bot.event
async def on_ready():

    """
    Run when you initiate this bot
    """

    global result,channel

    daily_task_checker.start()
    task_reminder.start()

    print("-"*20)
    print("Bot enabled")
    print("discord ver. :",discord.__version__) 
    print("-"*20)

    result = []


@bot.command()
async def set_channel(ctx):

    """
    Set the channel on which the bot sends messages
    """
    
    global channel
    channel = ctx.channel
    await ctx.send(f"set the channel for sending messages to {channel.mention}")

@bot.command() 
async def add_task(ctx, message): # task, weekday, time

    """
    Add a task to the list.
        ・weekday should be int.(monday:0 ... sunday:6)
        ・time should be "1800"
    ex) !add_task(task, weekday, time)
    """

    global channel
    task_data = message.split(",")

    valid, error_message = validate_input(task_data)
    if not valid:
        await channel.send(error_message)
        return
    
    task.append(task_data)

    dt_now = datetime.now()
    now = dt_now.strftime("%H%M")
    weekday = dt_now.weekday()
    if int(task_data[1]) == int(weekday) and int(task_data[2]) > int(now):
        result.append(task_data)

    await channel.send(f"Task '{task_data[0]}' added for {weekday_dic[int(task_data[1])]} at {task_data[2]}")

@bot.command()
async def delete_task(ctx,message):

    """
    Delete task by /delete TaskName
    """

    for x in task:
        if message in x[0]:
            task.remove(x)
            await channel.send(f"Deleted '{message}'")
        else:
            await channel.send(f"'{message}' was not on the list. ")

@bot.command()
async def show_task(ctx):

    """
    Current task list
    """

    global channel
    task.sort(key=lambda x: (x[1],x[2]))
    await channel.send("> Task   Weekday   Time")
    await channel.send("> ----------------------")
    for x in task:
        await channel.send(f"> {x[0]}   {weekday_dic[int(x[1])]}   {x[2]}")

bot.run(TOKEN)