from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards import main_menu

router = Router(name=__name__)


@router.message(CommandStart())
async def start_cmd(message: Message):
    text = '''Здравствуйте, этот тест направлен на определение вашего темперамента, что в дальнейшем поможет нам лучше определить ваш стиль одежды.

Для того, чтобы начать тест нажмите на кнопку "Начать тест"'''
    await message.answer(text, reply_markup=main_menu)
