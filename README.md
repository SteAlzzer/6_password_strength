# 6_password_strength
## Зачем нужен этот скрипт
Когда нужно оценить сложность придуманного пароля, можно обратиться к этому скрипту.
Десятибальная оценочная шкала экспертов диванного консорциума построена на личных предпочтениях и общедоступной информации в интернете

## Как использовать 
`python password_strength.py password [-v] [-b blacklist_filepath] [-t topnames_filepath] [-c topcompanies_filepath]`.
- `password` - Пароль. Если имеются пробелы, нужно указать в кавычках: `python password_strength.py "my Passw0rd 1s b1g"`;
- `-v (--verbose)` - Флаг для вывода более подробной информации;
- `-b (--blacklist)` - Путь до текстового файла blacklist. По умолчанию ./blacklist.txt
- `-t (--topnames)` - Путь до текстового файла top\_names. По умолчанию ./top_names.txt
- `-c (--topcompanies)` - Путь до текстового файла top\_companies. По умолчанию ./top_companies.txt