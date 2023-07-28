import os
import re
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from sympy import sympify, SympifyError
from dotenv import load_dotenv
import requests

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ["SLACK_BOT_TOKEN"], name="Nerdbot")


@app.command("/hello")
def handle_hello(say, command):
    say(f"Hey <@{command['user_id']}>!")


@app.event("member_joined_channel")
def welcome_message(event, say):
    say(f"Hey <@{event['user']}>! Welcome to {event['channel']}. :tada:")


@app.command("/nasa-pic")
def handle_nasa_pic(say):
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={os.environ['NASA_API_KEY']}")
    blocks = [
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": response.json()["title"]
            },
            "image_url": response.json()["url"],
            "alt_text": response.json()["title"]
        }
    ]
    say(blocks=blocks)


@app.command("/suggest-activity")
def handle_activity(say, command):
    activity = requests.get("https://www.boredapi.com/api/activity").json()
    say(f"Hey <@{command['user_id']}>, how about *{activity['activity']}*?")


@app.message(re.compile(r"^([-+*/^%!().\d\s]+)$"))
def calc(message, context, say):
    try:
        formula = context["matches"][0]
        result = sympify(formula)
        if result.is_Integer:
            answer = int(result)
        else:
            answer = float(result)
        say(f"Hey <@{message['user']}>, the answer is *{answer}*")
    except SympifyError:
        say(f"Hey <@{message['user']}>, I can't solve that :(")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
