import os
import re
import string
from optparse import OptionParser

blacklist_default_path = './blacklist.txt'
topnames_default_path = './top_names.txt'
topcompanies_default_path = './top_companies.txt'

def is_pass_case_sensivite(password):
    # the use of both upper-case and lower-case letters (case sensitivity)
    if not password.isupper() and not password.islower():
        return True
    return False


def is_pass_contains_digit(password):
    # inclusion of one or more numerical digits
    if re.search('[0-9]', password):
        return True
    return False


def is_pass_contains_specchar(password):
    # inclusion of special characters, such as @, #, $
    reg_exp_string = ''
    for char in string.punctuation:
        reg_exp_string += '\\' + char 
    if re.search(reg_exp_string, password):
        return True
    return False


def is_password_not_in_blacklist(password, blacklist_file_path):
    # prohibition of words found in a password blacklist
    password = password.lower()
    for line in open(blacklist_file_path):
        if line in password or password in line:
            return False
    return True

def is_pass_not_contains_famous_names(password, famous_names_list_file_path):
    # prohibition of words found in the user's personal information
    # Top 2,000 Baby Names
    # U.S. City Names
    # Top 100 Dog Names
    # Top 1,000 Word Cities (By Population)
    # U.S. State Names
    pass


def get_password_strength(password, blacklist_path, topnames_path, topcompanies_path):
    # prohibition of use of company name or an abbreviation
    # prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers, or other common numbers
    strenght = 0
    if len(password) > 12: # Вот такие вот рекомендации по длине пароля
        strenght += 1
    else:
        print(u'Ну и куда ты с такой фитюлькой? Увеличивай!')

    if is_pass_case_sensivite(password):
        strenght += 1
    else:
        print(u'Пароль должен быть регистро-разнообразным! (ПрИфКи иЗ 2007')
    if is_pass_contains_digit(password):
        strenght += 1
    else:
        print(u'Лучший пароль должен содержать цифры. А у тебя этого нет!')
    if is_pass_contains_specchar(password):
        strenght += 1
    else:
        print(u'Что нибудь слышал про !@#$%^&*( ?')

    if is_password_not_in_blacklist(password, blacklist_path):
        strenght += 1
    else:
        print(u'Уоу-уоу. Твой пароль в чёрном списке. Придумай что-нибудь пооригинальнее!')

    if is_pass_not_contains_famous_names(password, topnames_path):
        strenght += 1
    else:
        print(u'Ты чё! Никаких распространённых имён в пароле!')


    return strenght

if __name__ == '__main__':
    usage = 'Usage: %prog password'
    parser = OptionParser(usage=usage)
    parser.add_option('-b', '--blacklist', action='store', type='string', help='Путь до текстового файла blacklist. По умолчанию ./blacklist.txt')
    parser.add_option('-t', '--topnames', action='store', type='string', help='Путь до текстового файла top_names. По умолчанию ./top_names.txt')
    parser.add_option('-c', '--topcompanies', action='store', type='string', help='Путь до текстового файла top_companies. По умолчанию ./top_companies.txt')
    
    options, arguments = parser.parse_args()

    if options.blacklist:
        blacklist_path = os.path.abspath(options.blacklist)
        if not os.path.isfile(blacklist_path):
            print(u'Файл blacklist не найден')
            exit(-1)
    else:
        blacklist_path = os.path.abspath(blacklist_default_path)
        if not os.path.isfile(blacklist_path):
            print(u'Файл blacklist_default_path не найден')
            exit(-1)

    if options.topnames:
        topnames_path = os.path.abspath(options.topnames)
        if not os.path.isfile(topnames_path):
            print(u'Файл topnames не найден')
            exit(-1)
    else:
        topnames_path = os.path.abspath(topnames_default_path)
        if not os.path.isfile(topnames_path):
            print(u'Файл topnames_default_path не найден')
            exit(-1)

    if options.topcompanies:
        topcompanies_path = os.path.abspath(options.topcompanies)
        if not os.path.isfile(topcompanies_path):
            print(u'Файл topcompanies не найден')
            exit(-1)
    else:
        topcompanies_path = os.path.abspath(topcompanies_default_path)
        if not os.path.isfile(topcompanies_path):
            print(u'Файл topcompanies_default_path не найден')
            exit(-1)

    if len(arguments) != 1:
        print(u'Скрипту требуется только твой пароль, сынок. Постарайся в следующий раз сделать всё правильно')
        exit(-1)

    password_strength = get_password_strength(arguments[0], blacklist_path, topnames_path, topcompanies_path)
    print(u'Ваш пароль `{}` получил {} из 10 баллов по независимой оценочной шкале экспертов диванного консорциума'.format(arguments[0], password_strength))
