from aiogram.filters.callback_data import CallbackData


class AnswerCallbackData(CallbackData, prefix='question'):
    index: int
    type: int
    answer_weight: float
