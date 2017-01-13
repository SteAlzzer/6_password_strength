import os
import re
import string
from optparse import OptionParser

# Config
blacklist_default_path = './blacklist.txt'
topnames_default_path = './top_names.txt'
topcompanies_default_path = './top_companies.txt'
#########


def is_pass_long_enough(password):
    '''
    Функция проверяет пароль на длину
    '''
    if len(password) > 12:
        return True
    else:
        return False


def is_pass_case_sensivite(password):
    '''
    the use of both upper-case and lower-case letters (case sensitivity)
    '''
    if not password.isupper() and not password.islower():
        return True
    else:
        return False


def is_pass_contains_digit(password):
    '''
    inclusion of one or more numerical digits
    '''
    if re.search('[0-9]', password):
        return True
    else:
        return False


def is_pass_contains_specchar(password):
    '''
    inclusion of special characters, such as @, #, $
    '''
    reg_exp_string = '['
    for char in string.punctuation:
        reg_exp_string += '\\' + char
    reg_exp_string += ']'
    if re.search(reg_exp_string, password):
        return True
    else:
        return False


def is_password_not_in_blacklist(password, blacklist_file_path=blacklist_default_path):
    '''
    prohibition of words found in a password blacklist
    '''
    lower_password = password.lower()
    for line in open(blacklist_file_path):
        lower_line = line.lower().rstrip('\n\r')
        if lower_line in lower_password or lower_password in lower_line:
            return line
    return True


def is_pass_not_contains_famous_names(password, famous_names_list_file_path=topnames_default_path):
    '''
    prohibition of words found in the user's personal information
    Top 2,000 Baby Names
    U.S. City Names
    Top 100 Dog Names
    Top 1,000 Word Cities (By Population)
    U.S. State Names
    '''
    lower_password = password.lower()
    for line in open(famous_names_list_file_path):
        lower_line = line.lower().rstrip('\n\r')
        if lower_line in lower_password or lower_password in lower_line:
            return line
    return True


def is_pass_not_contains_topcompanies(password, topcompanies_list_file_path=topcompanies_default_path):
    '''
    prohibition of use of company name or an abbreviation
    '''
    lower_password = password.lower()
    for line in open(topcompanies_list_file_path):
        lower_line = line.lower().rstrip('\n\r')
        if (lower_line in lower_password) or (lower_password in lower_line):
            return line
    return True


def is_number_between_values(number, low, high):
    '''
    Функция проверяет, попадает ли число в заданный интервал
    '''
    if int(number) >= low and int(number) <= high:
        return True
    else:
        return False


def is_number_outside_values(number, low, high):
    '''
    Функция проверяет, не попадает ли число в заданный интервал
    '''
    if int(number) >= high or int(number) <= low:
        return True
    else:
        return False


def check_four_digits_for_month_and_day(four_digit_number):
    '''
    Функция проверяет четырехзначное число на соответсвие формату mmdd или ddmm
    '''
    assert isinstance(four_digit_number, str) and len(four_digit_number) == 4
    first_part, second_part = four_digit_number[:2], four_digit_number[2:]
    if int(first_part) in range(1, 12) and int(second_part) in range(1, 31):
        return True
    elif int(second_part) in range(1, 12) and int(first_part) in range(1, 31):
        return True
    else:
        return False


def is_pass_not_match_calendar_date(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    for found_regexp in re.finditer(r'\d\d\d\d', password):
        found_four_digits = found_regexp.group(0)
        if is_number_between_values(found_four_digits, 1900, 2017):
            return found_four_digits
        elif check_four_digits_for_month_and_day(found_four_digits):  # Попытаемся определить, является ли \d\d комбинацией месяца и числа
            return found_four_digits

    for found_regexp in re.finditer(r'\d\d', password):
        found_two_digits = found_regexp.group(0)
        if is_number_outside_values(found_two_digits, 17, 70):
            return found_two_digits
    return True


def is_pass_not_match_license_plate(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    license_plate_number = re.search('[АВЕКМНОРСТУХABEKMHOPCTYX][0-9]{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}([0-9]{1,3})?', password, re.I)
    if license_plate_number:
        return license_plate_number.group(0)
    else:
        return True


def is_pass_not_match_phone_number(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    phone_number = re.search('((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', password)  # Решил не мудрить и честно стыбзил с интернетов
    if phone_number:
        return phone_number.group(0)
    else:
        return True


def check_pass_for_signature(password, signature_function, success_message, failure_message, verbose=False):
    '''
    Функция, проверяющие переданную сигнатуру на пароле.
    '''
    signature_result = signature_function(password)
    if signature_result is True:
        if verbose:
            print(success_message)
        return True
    else:
        if signature_result is False:
            print(failure_message)
        else:
            print(failure_message.format(signature_result))
        return False


def create_signature_entity(function_name, success_message, failure_message):
    '''
    Функция для формирования словаря с сигнатурами
    '''
    signature = {}
    signature['function_name'] = function_name
    signature['success_message'] = success_message
    signature['failure_message'] = failure_message
    return signature


def init_signatures():
    '''
    Функция для инициализации сигнатур
    '''
    signatures = []
    signatures.append(create_signature_entity(
        is_pass_long_enough, u'>>> Пароль прошёл проверку на длину',
        u'Ну и куда ты с такой фитюлькой? Увеличивай!'))
    signatures.append(create_signature_entity(
        is_pass_case_sensivite, u'>>> Пароль прошёл проверку на регистрозависимость',
        u'Пароль должен быть регистро-разнообразным! (ПрИфКи иЗ 2007)'))
    signatures.append(create_signature_entity(
        is_pass_contains_digit, u'>>> Пароль прошёл проверку на наличие цифр',
        u'Лучший пароль должен содержать цифры. А у тебя этого нет!'))
    signatures.append(create_signature_entity(
        is_pass_contains_specchar, u'>>> Пароль прошёл проверку на наличие спец-символов',
        u'Что нибудь слышал про !@#$%^&*( ?'))
    signatures.append(create_signature_entity(
        is_password_not_in_blacklist, u'>>> Пароль прошёл проверку на blacklist',
        u'Уоу-уоу. Твой пароль в чёрном списке. Придумай что-нибудь пооригинальнее! Вот что мы нашли: {}'))
    signatures.append(create_signature_entity(
        is_pass_not_contains_famous_names, u'>>> Пароль прошёл проверку на наличие распространённых имён',
        u'Ты чё! Никаких распространённых имён в пароле! Вот что мы нашли: {}'))
    signatures.append(create_signature_entity(
        is_pass_not_contains_topcompanies, u'>>> Пароль прошёл проверку на наличие имён известных компаний',
        u'Не стоит указывать в пароле имена компаний, которые у  на слуху. Вот что мы нашли: {}'))
    signatures.append(create_signature_entity(
        is_pass_not_match_calendar_date, u'>>> Пароль прошёл проверку на наличие даты',
        u'Для опытного сыщика не составит труда найти твою дату рождения. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))
    signatures.append(create_signature_entity(
        is_pass_not_match_license_plate, u'>>> Пароль прошёл проверку на наличие автомобильного номера',
        u'Для опытного сыщика не составит труда найти твой номер автомобиля. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))
    signatures.append(create_signature_entity(
        is_pass_not_match_phone_number, u'>>> Пароль прошёл на наличие мобильного телефона',
        u'Для опытного сыщика не составит труда найти твой телефонный номер. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'))

    return signatures


def get_password_strength(password, verbose=False):
    '''
    Функция для оценки сложности пароля
    '''
    strenght = 0
    signatures = init_signatures()

    for signature in signatures:
        if check_pass_for_signature(password, signature['function_name'], signature['success_message'], signature['failure_message'], verbose=verbose):
            strenght += 1

    return strenght


def validate_option_for_file(filepath, default_filepath, filename):
    '''
    Вспомогательная функция для валидации передаваемых через аргументы путей файлов
    '''
    if filepath:
        result_path = os.path.abspath(filepath)
        if not os.path.isfile(result_path):
            print(u'Файл {} не найден'.format(filename))
            exit(-1)
    else:
        result_path = os.path.abspath(default_filepath)
        if not os.path.isfile(result_path):
            print(u'Файл по умолчанию {} не найден'.format(filename))
            exit(-1)

    return result_path


def main(options, arguments):
    if len(arguments) != 1:
        print(u'Скрипту требуется только твой пароль, сынок. Постарайся в следующий раз сделать всё правильно')
        exit(-1)

    password_strength = get_password_strength(arguments[0], options.verbose)
    print('---\n')
    print(u'Ваш пароль `{}` получил {} из 10 баллов по независимой оценочной шкале экспертов диванного консорциума'.format(arguments[0], password_strength))


if __name__ == '__main__':
    usage = 'Usage: %prog password [-v] [-b blacklist_filepath] [-t topnames_filepath] [-c topcompanies_filepath]'
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Выводить чуть больше информации')

    options, arguments = parser.parse_args()

    main(options, arguments)
