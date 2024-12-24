from discord.ext import commands
import discord
import os

from database import engine, Message
from sqlmodel import Session
from random import choice, random
from datetime import datetime
import asyncio

from random import randint
from dotenv import load_dotenv
load_dotenv()

def run_discord_bot():
   import discord
from discord.ext import commands

# Enable all intents, including the message content intent
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

   

@bot.event
async def on_ready():
        print(f"Logged in as {bot.user}")
        
        from discord.ext import commands

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True  # Ensure this is enabled
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Add a hello command
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.name}!")

@bot.command()
async def ping(ctx):
        await ctx.send("Pong!")

@bot.command()
async def roll(ctx, sides: int = 6):
    """Roll a die with a given number of sides (default is 6)."""
    if sides < 1:
        await ctx.send("The die must have at least 1 side!")
    else:
        result = choice(range(1, sides + 1))
        await ctx.send(f"🎲 You rolled a {result}!")

@bot.command()
async def greet(ctx):
    """Sends a random greeting."""
    greetings = [
        f"Hello, {ctx.author.mention}!",
        "Hey there! 👋",
        "What's up?",
        "Hi! Hope you're having a great day!",
    ]
    await ctx.send(choice(greetings))

@bot.command()
async def time(ctx):
    """Tells the current time."""
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"The current time is {formatted_time}")

@bot.command()
async def rps(ctx, choice: str):
    """Play Rock, Paper, Scissors with the bot."""
    rps_choices = ["rock", "paper", "scissors"]
    bot_choice = choice(rps_choices)

    if choice.lower() not in rps_choices:
        await ctx.send("Please choose rock, paper, or scissors!")
    else:
        await ctx.send(f"I chose {bot_choice}.")
        if choice.lower() == bot_choice:
            await ctx.send("It's a tie!")
        elif (
            (choice.lower() == "rock" and bot_choice == "scissors") or
            (choice.lower() == "paper" and bot_choice == "rock") or
            (choice.lower() == "scissors" and bot_choice == "paper")
        ):
            await ctx.send("You win! 🎉")
        else:
            await ctx.send("I win! 😎")

@bot.command()
async def motivate(ctx):
    """Sends a motivational quote."""
    quotes = [
        "Believe in yourself and all that you are.",
        "Your only limit is your mind.",
        "Dream it. Wish it. Do it.",
        "Stay positive, work hard, and make it happen!",
        "Success doesn’t come to you, you go to it."
    ]
    await ctx.send(choice(quotes))


@bot.event
async def on_message(message):
        if not message.author.bot:
            with Session(engine) as session:
                new_message = Message(
                    author=str(message.author),
                    text=message.content,
                    session_id=1  # Update with actual logic
                )
                session.add(new_message)
                session.commit()
        await bot.process_commands(message)
 
@bot.command()
async def trivia(ctx):
    """A simple trivia question."""
    questions = {
        "What is the capital of France?": "paris",
        "What is 5 + 7?": "12",
        "Who wrote 'To Kill a Mockingbird'?": "harper lee",
        "What is the chemical symbol for water?": "h2o",
        "Who painted the Mona Lisa?": "leonardo da vinci"
    }
    question, answer = choice(list(questions.items()))
    await ctx.send(f"🧠 Trivia Time! {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=15.0, check=check)
        if msg.content.lower() == answer:
            await ctx.send("🎉 Correct!")
        else:
            await ctx.send(f"❌ Wrong! The correct answer was '{answer}'.")
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ Time's up! The correct answer was '{answer}'.")

@bot.command()
async def guess(ctx):
    """Guess the number game."""
    number = randint(1, 100)
    await ctx.send("🎲 I'm thinking of a number between 1 and 100. Try to guess it!")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    for _ in range(5):  # Allow 5 attempts
        try:
            msg = await bot.wait_for("message", timeout=10.0, check=check)
            guess = int(msg.content)
            if guess == number:
                await ctx.send(f"🎉 You guessed it! The number was {number}.")
                return
            elif guess < number:
                await ctx.send("🔼 Higher!")
            else:
                await ctx.send("🔽 Lower!")
        except asyncio.TimeoutError:
            await ctx.send("⏰ You took too long to guess!")
            return

    await ctx.send(f"❌ Out of attempts! The number was {number}.")

@bot.command()
async def choose(ctx, *choices):
    """Choose randomly from provided options."""
    if not choices:
        await ctx.send("❌ You need to provide some choices!")
    else:
        await ctx.send(f"🤔 I choose: {choice(choices)}")

@bot.command()
async def echo(ctx, *, message):
    """Echoes back the message."""
    await ctx.send(message)

@bot.command()
async def countdown(ctx, seconds: int):
    """Countdown timer."""
    if seconds > 60:
        await ctx.send("❌ That's too long! Keep it under 60 seconds.")
    else:
        await ctx.send(f"⏳ Starting countdown: {seconds} seconds...")
        for i in range(seconds, 0, -1):
            await ctx.send(i)
            await asyncio.sleep(1)
        await ctx.send("🎉 Time's up!")     
 
 # Reminder Command
@bot.command()
async def remind(ctx, time: int, *, message: str):
    try:
        await ctx.send(f"⏰ Reminder set! I'll remind you in {time} seconds: *{message}*")
        await asyncio.sleep(time)
        await ctx.send(f"🔔 Reminder: {message}")
    except:
        await ctx.send("❌ Could not set the reminder. Please try again.")

  
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set in the environment")

bot.run(BOT_TOKEN)
