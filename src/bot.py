import logging
from aiogram import Dispatcher
from factories import bot
from telegram.handlers import router


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s- %(message)s')

    dp = Dispatcher()
    dp.include_router(router)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()