import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ["SLACK_BOT_TOKEN"], name="Nerdbot")


# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(text=f"Hey there <@{message['user']}>!")
    logger.info(f"Message sent to {message['channel']}")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
