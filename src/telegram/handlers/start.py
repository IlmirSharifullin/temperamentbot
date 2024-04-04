from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards import main_menu

router = Router(name=__name__)


@router.message(CommandStart())
async def start_cmd(message: Message):
    text = 'Текст для старта'
    await message.answer(text, reply_markup=main_menu)
