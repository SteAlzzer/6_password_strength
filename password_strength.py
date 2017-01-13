import os
import re
import string
from optparse import OptionParser

blacklist_default_path = './blacklist.txt'
topnames_default_path = './top_names.txt'
topcompanies_default_path = './top_companies.txt'


def is_pass_case_sensivite(password):
    '''
    the use of both upper-case and lower-case letters (case sensitivity)
    '''
    if not password.isupper() and not password.islower():
        return True
    return False


def is_pass_contains_digit(password):
    '''
    inclusion of one or more numerical digits
    '''
    if re.search('[0-9]', password):
        return True
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
    return False


def is_password_not_in_blacklist(password, blacklist_file_path):
    '''
    prohibition of words found in a password blacklist
    '''
    lower_password = password.lower()
    for line in open(blacklist_file_path):
        lower_line = line.lower().rstrip('\n\r')
        if lower_line in lower_password or lower_password in lower_line:
            return line
    return True


def is_pass_not_contains_famous_names(password, famous_names_list_file_path):
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


def is_pass_not_contains_topcompanies(password, topcompanies_list_file_path):
    '''
    prohibition of use of company name or an abbreviation
    '''
    lower_password = password.lower()
    for line in open(topcompanies_list_file_path):
        lower_line = line.lower().rstrip('\n\r')
        if (lower_line in lower_password) or (lower_password in lower_line):
            return line
    return True


def is_pass_not_match_calendar_date(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    for found_regexp in re.finditer(r'\d\d\d\d', password):
        found_four_digits = found_regexp.group(0)
        if int(found_four_digits) > 1900 and int(found_four_digits) < 2017:
            return found_four_digits
        else:  # Попытаемся определить, является ли \d\d комбинацией месяца и числа
            first_part, second_part = found_four_digits[:2], found_four_digits[2:]
            if int(first_part) in range(1, 12) and int(second_part) in range(1, 31):
                return found_four_digits
            elif int(second_part) in range(1, 12) and int(first_part) in range(1, 31):
                return found_four_digits

    for found_regexp in re.finditer(r'\d\d', password):
        found_two_digits = found_regexp.group(0)
        if int(found_two_digits) > 70 or int(found_two_digits) < 16:
            return found_two_digits
    return True


def is_pass_not_match_license_plate(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    license_plate_number = re.search('[АВЕКМНОРСТУХABEKMHOPCTYX][0-9]{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}([0-9]{1,3})?', password, re.I)
    if license_plate_number:
        return license_plate_number.group(0)
    return True


def is_pass_not_match_phone_number(password):
    '''
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers
    '''
    phone_number = re.search('((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', password)  # Решил не мудрить и честно стыбзил с интернетов
    if phone_number:
        return phone_number.group(0)
    return True


def get_password_strength(password, blacklist_path, topnames_path, topcompanies_path, verbose=False):
    '''
    Функция для оценки сложности пароля
    '''
    strenght = 0
    if len(password) > 12:  # Вот такие вот рекомендации по длине пароля
        strenght += 1
        if verbose: print(u'>>>  Пароль прошёл проверку на длину')
    else:
        print(u'Ну и куда ты с такой фитюлькой? Увеличивай!')

    if is_pass_case_sensivite(password):
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на регистрозависимость')
    else:
        print(u'Пароль должен быть регистро-разнообразным! (ПрИфКи иЗ 2007')

    if is_pass_contains_digit(password):
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие цифр')
    else:
        print(u'Лучший пароль должен содержать цифры. А у тебя этого нет!')
    if is_pass_contains_specchar(password):
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие спец-символов')
    else:
        print(u'Что нибудь слышал про !@#$%^&*( ?')

    res = is_password_not_in_blacklist(password, blacklist_path)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на blacklist')
    else:
        print(u'Уоу-уоу. Твой пароль в чёрном списке. Придумай что-нибудь пооригинальнее! Вот что мы нашли: {}'.format(res))

    res = is_pass_not_contains_famous_names(password, topnames_path)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие распространённых имён')
    else:
        print(u'Ты чё! Никаких распространённых имён в пароле! Вот что мы нашли: {}'.format(res))

    res = is_pass_not_contains_topcompanies(password, topcompanies_path)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие имён известных компаний')
    else:
        print(u'Не стоит указывать в пароле имена компаний, которые у всех на слуху. Вот что мы нашли: {}'.format(res))

    res = is_pass_not_match_calendar_date(password)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие даты')
    else:
        print(u'Для опыного сыщика не составит труда найти твою дату рождения. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'.format(res))

    res = is_pass_not_match_license_plate(password)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл проверку на наличие автомобильного номера')
    else:
        print(u'Для опыного сыщика не составит труда найти твой номер автомобиля. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'.format(res))

    res = is_pass_not_match_phone_number(password)
    if res is True:
        strenght += 1
        if verbose: print(u'>>> Пароль прошёл на наличие мобильного телефона')
    else:
        print(u'Для опыного сыщика не составит труда найти твой телефонный номер. Не стоит использовать подобные сведения в пароле. Вот что мы нашли: {}'.format(res))

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
    blacklist_path = validate_option_for_file(options.blacklist, blacklist_default_path, 'blacklist')
    topnames_path = validate_option_for_file(options.topnames, topnames_default_path, 'topnames')
    topcompanies_path = validate_option_for_file(options.topcompanies, topcompanies_default_path, 'topcompanies')

    if len(arguments) != 1:
        print(u'Скрипту требуется только твой пароль, сынок. Постарайся в следующий раз сделать всё правильно')
        exit(-1)

    password_strength = get_password_strength(arguments[0], blacklist_path, topnames_path, topcompanies_path, options.verbose)
    print('---\n')
    print(u'Ваш пароль `{}` получил {} из 10 баллов по независимой оценочной шкале экспертов диванного консорциума'.format(arguments[0], password_strength))


if __name__ == '__main__':
    usage = 'Usage: %prog password [-v] [-b blacklist_filepath] [-t topnames_filepath] [-c topcompanies_filepath]'
    parser = OptionParser(usage=usage)
    parser.add_option('-b', '--blacklist', action='store', type='string', help='Путь до текстового файла blacklist. По умолчанию ./blacklist.txt')
    parser.add_option('-t', '--topnames', action='store', type='string', help='Путь до текстового файла top_names. По умолчанию ./top_names.txt')
    parser.add_option('-c', '--topcompanies', action='store', type='string', help='Путь до текстового файла top_companies. По умолчанию ./top_companies.txt')
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Выводить чуть больше информации')

    options, arguments = parser.parse_args()

    main(options, arguments)
