from typing import TypedDict

from aiogram import Bot
from src.settings import settings


class Answer(TypedDict):
    text: str
    weight: float


class Question(TypedDict):
    index: int
    question: str
    type: int
    answers: list[Answer]


TYPES = ["Флегматик", "Меланхолик", "Холерик", "Сангвиник"]
bot = Bot(settings.bot_token)
