# Discord Task Reminder Bot

This is a Discord bot that sends reminders for tasks and deadlines. It can add new tasks to a list, display the current list of tasks, and send reminders when a task is due or approaching the deadline.

### Installing

    Clone this repository to your local machine.
    Install the required packages.
    Create a new Discord bot account and get its token.
    Create a .env file in the root directory of the project, and add the following line: TOKEN=<your bot token>, channel=<your guild channel>
    Set up the bot by running the bot.py file: python bot.py.

### Usage

To use the bot, type !help in the Discord server to see a list of available commands.

    !set_channel: Set the channel on which the bot sends messages.
    !add_task (task, weekday, time): Add a task to the list. Weekday should be an integer (0-6, where 0 is Monday and 6 is Sunday), and time should be in 24-hour format (e.g. "1800").
    !delete_task: Delete the specified task from the task list.
    !show_task: Display the current list of tasks.

### Developer

    Garyo99

### Disclaimer:
The use of this Discord bot is at your own risk. The author of this bot is not responsible for any damages or losses that may arise from the use of this bot.
