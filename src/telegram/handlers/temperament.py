from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..keyboards import get_question_keyboard
from ..states import TemperamentStatesGroup
from src.factories import Question
from src.questions.parser import get_question, QUESTIONS_COUNT
from ..callback_datas import AnswerCallbackData

router = Router(name=__name__)


@router.message(F.text == 'Начать тест')
async def start_test(message: Message, state: FSMContext):
    text = 'Начало теста'
    await message.answer(text)
    await state.clear()
    current: Question = get_question(1)

    if current is None:
        return await message.answer('Ошибка! Вопросов почему-то нет;( Попробуйте позже..')

    await state.set_state(TemperamentStatesGroup.temperament)
    await state.set_data({"answers": [0, 0, 0, 0]})

    kb = get_question_keyboard(current)
    text = f'{current.get("index")} / {QUESTIONS_COUNT}. {current.get("question")}'
    await message.answer(text=text, reply_markup=kb)


@router.callback_query(AnswerCallbackData.filter(), TemperamentStatesGroup.temperament)
async def answer(query: CallbackQuery, callback_data: AnswerCallbackData, state: FSMContext):
    data = await state.get_data()
    answers = data.get('answers')
    answers[callback_data.type] += callback_data.answer_weight
    await state.update_data(answers=answers)

    next_question = get_question(callback_data.index + 1)
    if next_question is None:
        ans = []
        answers_sum = sum(answers)
        phlegmatic_score = int(answers[0] / answers_sum * 100)
        melancholic_score = int(answers[1] / answers_sum * 100)
        choleric_score = int(answers[2] / answers_sum * 100)
        sanguine_score = int(answers[3] / answers_sum * 100)
        if phlegmatic_score >= 30:
            ans.append('''Флегматик. Новые формы поведения вырабатываются медленно, но являются стойкими.
Обладает медлительностью и спокойствием в действиях, мимике и речи, ровностью,
постоянством, глубиной чувств и настроений. Настойчивый и упорный, он редко выходит
из себя, не склонен к аффектам, рассчитав свои силы, доводит дело до конца, ровен в
отношениях, в меру общителен, не любит попусту болтать. Экономит силы, попусту их не
тратит. В зависимости от условий в одних случаях флегматик может характеризоваться
"положительными" чертами - выдержкой, глубиной мыслей, постоянством,
основательностью, в других - ленью и склонностью к выполнению одних лишь
привычных действий.''')
        if melancholic_score >= 30:
            ans.append('''Меланхолик. Обладает высокой чувствительностью: присутствует глубина чувств при
слабом их выражении. Ему свойственна сдержанность и приглушенность речи и
движений, скромность, осторожность. В нормальных условиях меланхолик - человек
глубокий, содержательный, ответственный, успешно справляться с жизненными задачами.
При неблагоприятных условиях может превратиться в замкнутого, тревожного, ранимого
человека, склонного к тяжелым внутренним переживаниям таких жизненных
обстоятельств, которые этого не заслуживают.''')
        if choleric_score >= 30:
            ans.append('''Холерик. Отличается повышенной возбудимостью, действия прерывисты. Ему
свойственны резкость и стремительность движений, сила, импульсивность, яркая
выраженность эмоциональных переживаний. Вследствие неуравновешенности, увлекшись
делом, склонен действовать изо всех сил, истощаться больше, чем следует. Имея
общественные интересы, темперамент проявляет в инициативности, энергичности,
принципиальности. При отсутствии духовной жизни холерический темперамент часто
проявляется в раздражительности, вспыльчивости при эмоциональных обстоятельствах.''')
        if sanguine_score >= 30:
            ans.append('''Сангвиник. Быстро приспосабливается к новым условиям, быстро сходится с людьми,
общителен. Чувства легко возникают и сменяются, эмоциональные переживания, как
правило неглубоки. Мимика богатая, подвижная, выразительная. Несколько непоседлив,
нуждается в новых впечатлениях, недостаточно регулирует свои импульсы, не умеет
строго придерживаться выработанного распорядка жизни, системы в работе. В связи с
этим не может успешно выполнять дело, требующее равной затраты сил, длительного и
методичного напряжения, усидчивости, устойчивости внимания, терпения. При
отсутствии серьезных целей, глубоких мыслей, творческой деятельности вырабатывается
поверхностность и непостоянство.''')
        if len(ans) == 4 or len(ans) == 0:
            text = 'Результаты теста неоднозначны, Вам присуще все темпераменты. Попробуйте пройти тест еще раз.'
        else:
            text = 'Результаты теста. Вам присуще следующие темпераменты:\n' + '\n'.join(ans)
            text += '\nЕсли вы хотите пройти тест еще раз, можете нажать кнопку "Начать тест"'
        print(phlegmatic_score, melancholic_score, choleric_score, sanguine_score, answers_sum)
        await query.message.edit_text(text, reply_markup=None)
        await state.clear()
        return

    print(callback_data.index, answers)

    kb = get_question_keyboard(next_question)
    text = f'{next_question.get("index")} / {QUESTIONS_COUNT}. {next_question.get("question")}'
    await query.message.edit_text(text=text, reply_markup=kb)
