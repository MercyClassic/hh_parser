import os

from dotenv import load_dotenv

from bot.main import bot

load_dotenv()

to_notificate = os.getenv('TO_NOTIFICATE')


async def send_notification(link: str) -> None:
    await bot.send_message(
        to_notificate,
        link,
    )
