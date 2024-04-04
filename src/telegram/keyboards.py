from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.factories import Question
from src.telegram.callback_datas import AnswerCallbackData

main_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                keyboard=[[KeyboardButton(text='Начать тест')]])


def get_question_keyboard(question: Question):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for i, answer in enumerate(question.get("answers")):
        kb.inline_keyboard.append([
            InlineKeyboardButton(text=answer.get('text'),
                                 callback_data=AnswerCallbackData(index=question.get('index'),
                                                                    type=question.get('type'),
                                                                    answer_weight=answer.get('weight')).pack())
        ])
    return kb
