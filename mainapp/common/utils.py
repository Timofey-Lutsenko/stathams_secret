import re

from pymongo import MongoClient


# Октрытие соединения с БД и получение документа
CLIENT = MongoClient('localhost', 27017)
DB = CLIENT['test_db']
CURRENT_COLLECTION = DB['mainapp_sample']
DB_DATA = CURRENT_COLLECTION.find_one()

# Получение из базы массива с шаблонами.
TEMPLATES = DB_DATA.get('data')


# Функция ищущая совпадения
# по шаблонам в базе данных.
def database_handler(request):
    for template in TEMPLATES:
        print(template)
        temp_dict = template.items()
        i = 0
        curr_name = ''
        for req in request.items():
            for el in temp_dict:
                if el[0] == 'name':
                    curr_name = el[1]
                if req[0] == el[0] \
                        and req[1] == el[1]:
                    i += 1

        if len(temp_dict) - 1 == i:
            return curr_name
    return str(request)


# Функция валидирующая дату.
# Получает на вход строчку с датой и
# Проверяет на соотвествие шаблону
# dd.mm.yyyy или yyyy-mm-dd
# Регулярного выражения.
# Возвращает тип 'date' или False.
def date_validator(date):
    date_template = re.compile(
        r'(\d{4}[--]\d{2}[--]\d{2}$)|'
        r'(\d{2}[-.]\d{2}[-.]\d{4}$)'
    )
    is_ok = re.fullmatch(date_template, date)
    if is_ok:
        return 'date'
    else:
        return False


# Функция валидирующая email
# Получает на вход строчку с почтой и
# Проверяет на соотвествие шаблону
# somestr@somestr.str
# Регулярного выражения.
# Возвращает тип 'email' или False.
def email_validator(data):
    email_template = re.compile(r'^[\w.]+@([\w-]+\.)+[\w-]{2,4}$')
    is_ok = re.fullmatch(email_template, data)
    if is_ok:
        return 'email'
    else:
        return False


# Функция нормализации телефонного номера.
# Функция преобразует строку с номером
# в список симфолов, после чего
# проверяет элементы на соответствие
# нежелательным символам из списка и удаляет их.
# Возвращает нормализованный номер в виде строки
def phone_normalizer(phone):
    phone_as_list = [symbol for symbol in phone]
    restricted_symbols = ['(', ')', ' ', '-']
    if not phone_as_list[0] == '+':
        return False
    for el in phone_as_list:
        if el in restricted_symbols:
            phone_as_list.remove(el)
    for el in phone_as_list[1:]:
        if not el.isdigit():
            return False
    normalized_number = ''.join(el for el in phone_as_list)
    return normalized_number


# Функция валидирующая номер.
# вызывает функцию нормализации номера
# Проверяет соотвествие номера регулярному выражению
# Возвращает тип 'phone' или False.
def phone_validator(phone_number):
    if phone_normalizer(phone_number):
        num = phone_normalizer(phone_number)
        phone_template = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
        is_ok = re.fullmatch(phone_template, num)
        if is_ok:
            return 'phone'
    else:
        return False


# Список функций валидаторов.
validators = [
            date_validator,
            email_validator,
            phone_validator
        ]


def fields_validator(user_request):
    separated_params = user_request.items()
    answer = []
    for el in separated_params:
        for value in el[1]:
            default_type = 'str'
            for validator in validators:
                validated_type = validator(value)
                if validated_type:
                    default_type = validated_type
                    break
            answer.append((el[0], default_type))

    return dict(answer)


# '+' = %2B
