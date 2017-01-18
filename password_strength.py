import os
import re
import string
from optparse import OptionParser

# Config
#########
# filepathes
blacklist_default_path = './blacklist.txt'
topnames_default_path = './top_names.txt'
topcompanies_default_path = './top_companies.txt'
#########
# default numberic values
min_length_for_password = 12
first_month_number, last_month_number = 1, 12
first_day_number_of_month, last_day_number_of_month = 1, 31
four_digit_year_start, four_digit_year_stop = 1900, 2017
two_digit_year_min, two_digit_year_max = 17, 70
#########


def is_pass_long_enough(password):
    return (len(password) > min_length_for_password, )


def is_pass_case_sensivite(password):
    return (not password.isupper() and not password.islower(), )


def is_pass_contains_digit(password):
    return (bool(re.search('[0-9]', password)), )


def is_pass_contains_specchar(password):
    reg_exp_string = '['
    for char in string.punctuation:
        reg_exp_string += '\\' + char
    reg_exp_string += ']'
    return (bool(re.search(reg_exp_string, password)), )


def compare_word_to_file(word, filepath):
    if not os.path.isfile(filepath):
        return False
    with open(filepath) as file_handler:
        content = file_handler.read().lower()
    return word in content


def is_password_not_in_blacklist(password, blacklist_file_path=blacklist_default_path):
    lower_password = password.lower()
    return (not compare_word_to_file(lower_password, blacklist_file_path), )


def is_pass_not_contains_famous_names(password, famous_names_list_file_path=topnames_default_path):
    lower_password = password.lower()
    return (not compare_word_to_file(lower_password, famous_names_list_file_path), )


def is_pass_not_contains_topcompanies(password, topcompanies_list_file_path=topcompanies_default_path):
    lower_password = password.lower()
    return (not compare_word_to_file(lower_password, topcompanies_list_file_path), )


def is_number_between_values(number, low_border, high_border):
    number_int = int(number)
    return number_int >= low_border and number_int <= high_border


def is_number_outside_values(number, low_border, high_border):
    number_int = int(number)
    return number_int >= high_border or number_int <= low_border


def check_four_digits_for_month_and_day(four_digit_number):
    assert isinstance(four_digit_number, str) and len(four_digit_number) == 4
    first_part, second_part = int(four_digit_number[:2]), int(four_digit_number[2:])
    if first_part in range(first_month_number, last_month_number) and \
       second_part in range(first_day_number_of_month, last_day_number_of_month):
        return True
    elif second_part in range(first_month_number, last_month_number) and \
         first_part in range(first_day_number_of_month, last_day_number_of_month):
        return True
    else:
        return False


def is_pass_not_match_calendar_date(password):
    for found_regexp in re.finditer(r'\d\d\d\d', password):
        found_four_digits = found_regexp.group(0)
        if is_number_between_values(found_four_digits, four_digit_year_start, four_digit_year_stop):
            return False, found_four_digits
        elif check_four_digits_for_month_and_day(found_four_digits):
            return False, found_four_digits

    for found_regexp in re.finditer(r'\d\d', password):
        found_two_digits = found_regexp.group(0)
        if is_number_outside_values(found_two_digits, two_digit_year_min, two_digit_year_max):
            return False, found_two_digits
    return (True,)


def is_pass_not_match_license_plate(password):
    license_plate_number = re.search('[АВЕКМНОРСТУХABEKMHOPCTYX][0-9]{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}([0-9]{1,3})?', password, re.I)
    if license_plate_number:  # Пытался сделать кракена, но не получилось -  return (bool(license_plate_number, license_plate_number.group(0) if license_plate_number else ...))
        return False, license_plate_number.group(0)
    else:
        return (True,)


def is_pass_not_match_phone_number(password):
    phone_number = re.search('((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', password)
    if phone_number:
        return (False, phone_number.group(0))
    else:
        return (True,)


def check_password_for_function(password, function_name, success_message, failure_message, verbose=False):
    '''
    Функция, проверяющие пароль на переданную функцию.
    '''
    function_result = function_name(password)

    if function_result[0]:
        if verbose:
            print(success_message)
        return True
    else:
        if len(function_result) == 2:
            print(failure_message.format(function_result[1]))
        else:
            print(failure_message)
        return False


def create_function_dict_entity(function_name, success_message, failure_message):
    '''
    Функция для формирования записи словаря для функции.
    Запись содержит имя функции и два сообщения
    '''
    function_dict_entity = {}
    function_dict_entity['function_name'] = function_name
    function_dict_entity['success_message'] = success_message
    function_dict_entity['failure_message'] = failure_message
    return function_dict_entity


def create_check_function_list():
    '''
    Функция для инициализации списка функций
    '''
    check_function_list = []
    check_function_list.append(create_function_dict_entity(
        is_pass_long_enough, '>>> Пароль прошёл проверку на длину',
        'Ну и куда ты с такой фитюлькой? Увеличивай!'))
    check_function_list.append(create_function_dict_entity(
        is_pass_case_sensivite, '>>> Пароль прошёл проверку на регистрозависимость',
        'Пароль должен быть регистро-разнообразным! (ПрИфКи иЗ 2007)'))
    check_function_list.append(create_function_dict_entity(
        is_pass_contains_digit, '>>> Пароль прошёл проверку на наличие цифр',
        'Лучший пароль должен содержать цифры. А у тебя этого нет!'))
    check_function_list.append(create_function_dict_entity(
        is_pass_contains_specchar, '>>> Пароль прошёл проверку на наличие спец-символов',
        'Что нибудь слышал про !@#$%^&*( ?'))
    check_function_list.append(create_function_dict_entity(
        is_password_not_in_blacklist, '>>> Пароль прошёл проверку на blacklist',
        'Уоу-уоу. Твой пароль в чёрном списке. Придумай что-нибудь пооригинальнее!'))
    check_function_list.append(create_function_dict_entity(
        is_pass_not_contains_famous_names, '>>> Пароль прошёл проверку на наличие распространённых имён',
        'Ты чё! Никаких распространённых имён в пароле!'))
    check_function_list.append(create_function_dict_entity(
        is_pass_not_contains_topcompanies, '>>> Пароль прошёл проверку на наличие имён известных компаний',
        'Не стоит указывать в пароле имена компаний, которые у  на слуху.'))
    check_function_list.append(create_function_dict_entity(
        is_pass_not_match_calendar_date, '>>> Пароль прошёл проверку на наличие даты',
        'Для опытного сыщика не составит труда найти твою дату рождения. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))
    check_function_list.append(create_function_dict_entity(
        is_pass_not_match_license_plate, '>>> Пароль прошёл проверку на наличие автомобильного номера',
        'Для опытного сыщика не составит труда найти твой номер автомобиля. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))
    check_function_list.append(create_function_dict_entity(
        is_pass_not_match_phone_number, '>>> Пароль прошёл на наличие мобильного телефона',
        'Для опытного сыщика не составит труда найти твой телефонный номер. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))

    return check_function_list


def get_password_strength(password, verbose=False):
    password_strenght = 0
    check_function_list = create_check_function_list()

    for function_dict in check_function_list:
        if check_password_for_function(password, function_dict['function_name'], function_dict['success_message'], function_dict['failure_message'], verbose=verbose):
            password_strenght += 1

    return password_strenght


def main(options, arguments):
    if len(arguments) != 1:
        print('Скрипту требуется только твой пароль, сынок. Постарайся в следующий раз сделать всё правильно')
        exit(-1)

    password_strength = get_password_strength(arguments[0], options.verbose)
    print('---\n')
    print('Ваш пароль `{}` получил {} из 10 баллов по независимой оценочной шкале экспертов диванного консорциума'.format(arguments[0], password_strength))


if __name__ == '__main__':
    usage = 'Usage: %prog password [-v]'
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Выводить чуть больше информации')

    options, arguments = parser.parse_args()

    main(options, arguments)
