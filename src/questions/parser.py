import json
from typing import Optional

from src.factories import Answer, Question, TYPES

STANDARD_ANSWERS = [Answer(text='Да', weight=1), Answer(text='Иногда', weight=0.5), Answer(text='Нет', weight=0)]


def parse(filename: str) -> dict[int, Question]:
    res = {}

    with open(filename) as f:
        data = f.read().split('\n\n')

    i = 1
    for typ, lines in enumerate(data):
        for question in lines.split('\n'):
            res[i] = Question(index=i, question=question, type=typ, answers=STANDARD_ANSWERS)
            i += 1
    return res


def save(data, filename: str = './questions.json'):
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get(filename: str = 'questions/questions.json'):
    with open(filename) as f:
        data = json.load(f)
    return data


def get_question(index: int) -> Optional[Question]:
    try:
        needed = Question(**QUESTIONS[str(index)])
        return needed
    except:
        return None


if __name__ == '__main__':
    data = parse('questions/questions.txt')
    save(data)

QUESTIONS = get('questions/questions.json')
QUESTIONS_COUNT = len(QUESTIONS)
