# -*- coding: cp1251 -*-
import subprocess
import pywinauto
import time

a = None
b = None


def quit_programm():
    print('До свидания')
    return


def first_key():
    fk = input(f'Введите пункт меню что хотим делать\n '
               f'1. Создать файл с адресами Проверьте наличие файла!!!\n '
               f'2. Получить адреса FQCN ключей\n'
               f' 3. Получить адреса JACARTA ключей\n'
               f' Введите номер пункта или q для выхода: ')
    if fk == '1':
        write_file()
    elif fk == '2' or fk == '3':
        read_file(fk)
    elif fk == 'q':
        quit_programm()
    else:
        first_key()


def login_inf():
    login = input('Введите логин для устройства: ')
    return login


def password_inf():
    password = input('Введите пароль для устройства: ')
    return password


def write_file():
    fk = input(f'Введите пункт меню что хотим делать\n '
               f'1. Создать файл с адресами ПОЛНЫЙ\n '
               f'2. Создать файл с адресами БЕЗ ИТБ КЛЮЧЕЙ\n'               
               f' Введите номер пункта или q для выхода: ')
    if fk == '2':
        cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys.txt"  # Здесь вместо date Ваша команда для git
        returned_output = subprocess.check_output(cmd)  # returned_output содержит вывод в виде строки байтов
        word = 'ИТБ'
        with open(f"c:\DKCL\\keys.txt", 'r+', encoding="utf8") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if word not in i:
                    f.write(i)
            f.truncate()
    elif fk == '1':
        cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys.txt"  # Здесь вместо date Ваша команда для git
        returned_output = subprocess.check_output(cmd)  # returned_output содержит вывод в виде строки байтов
        print('Сохранение в файл:', returned_output.decode("cp1251"))  # Преобразуем байты в строку

    elif fk == 'q':
        quit_programm()
    # cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys.txt"  # Здесь вместо date Ваша команда для git
    # returned_output = subprocess.check_output(cmd)  # returned_output содержит вывод в виде строки байтов
    # print('Сохранение в файл:', returned_output.decode("cp1251"))  # Преобразуем байты в строку
    first_key()


def write_new_file(fk):
    if fk == '2':  # Создаем файл в зависимости от ключа
        fn = 'fqcn'
    else:
        fn = 'jacarta'
    final = open(f"c:\DKCL\\Final_file_{fn}.txt", "w", encoding="cp1251")
    final.close()
    return fk


def read_file(fk):
    word = "-->"
    fk = write_new_file(fk)
    l = login_inf()
    p = password_inf()
    with open("c:\DKCL\\keys.txt", encoding="utf8") as file:  # Разбираем файл с ключами построчно
        for line in file:
            if word in line:
                f = line.split('   -->')
                f = f[1]
                f = f.split('(')
                a = f[0]
                print(a)
                f = f[1]
                f = f.replace(")", '')
                f = f.replace("\n", '')
                f = f.replace(" ", ',')
                if fk == '2':
                    b = fqcn_address(f, l, p)
                else:
                    b = jacarta_address(f, l, p)
                write_final_file(a, b, fk)
    return


def fqcn_address(f, l, p):
    cmd = f"C:\DKCL\dkcl64.exe -t \"USE,{f}{l}\\{p}\""  # 12345678 пароль пользователя
    subprocess.run(cmd)
    time.sleep(5)
    # Забираем UID ключа полный
    cmd = "C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys"
    returned_output = subprocess.check_output(cmd)
    b = returned_output.decode("cp866")
    print(b)
    start = -1
    count = 0
    count_all = b.count("Aladdin R.D. JaCarta")
    # print(count)

    while True:
        start = b.find("Aladdin R.D. JaCarta", start + 1)
        # print(b)
        if start == -1:
            break
        count += 1


    # Проход по ключам
    if count_all == 1:
        b = b.split('Aladdin R.D. JaCarta 0')
        i = 1
        d = []
        while i <= count:
            c = b[i]
            c = c.split('\n')
            d.append(c[0])
            i += 1
    else:
        b = b.split('Aladdin R.D. JaCarta 0')
        i = 1
        d = []
        while i <= count_all:
            c = b[i]
            c = c.split('\n')
            d.append(c[0])
            i += 1



    # i = 1
    # d = []
    # while i <= count:
    #     c = b[i]
    #     c = c.split('\n')
    #     d.append(c[0])
    #     i += 1

    # b = b.split(' ')
    # b = b[14]
    # b = b.replace('0\\','')
    # b = b.replace('\r\nOK.\r\nTotal:', '')  # Вытаскиваем ид ключа
    # # subprocess.check_output(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    time.sleep(3)
    return d


def jacarta_address(f, l, p):
    cmd = f"C:\DKCL\dkcl64.exe -t \"USE,{f}{l}\\{p}\""  # 12345678 пароль пользователя
    # subprocess.check_output(cmd)
    subprocess.run(cmd)
    time.sleep(5)
    # Забираем наименование Jacarta
    cmd = "C:\Program Files\Crypto Pro\CSP\csptest -keyset -enum_cont -verifycontext -uniq"  # bad
    returned_output = subprocess.check_output(cmd)
    b = returned_output.decode("cp1251")
    b = b.split('|SCARD')
    print(b)
    try:
        b = b[1]
        b = b.split('\\')
        b = b[1]
    except IndexError:
        print('Порт занят')
        b = 'JACARTA_Порт занят'
    else:
        subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
        time.sleep(3)
    return b


def write_final_file(a, b, fk):
    if fk == '2':
        # final = open(f"c:\DKCL\\Final_file_fqcn.txt", "a", encoding="cp1251")
        with open(f"c:\DKCL\\Final_file_fqcn.txt", "a", encoding="cp1251") as final:
            for i in b:
                # a = f'{a} - {b}\n'  # Выделение только адреса ключа
                final.write(f'{a} - {i}')
    else:
        final = open(f"c:\DKCL\\Final_file_jacarta.txt", "a", encoding="cp1251")
        b = b.replace('JACARTA_', '')
        a = f'{a} - {b}\n'  # Выделение только адреса ключа
        final.write(a)
    final.close()
    # final = open(f"c:\DKCL\\Final_file_{fk}.txt", "a", encoding="utf8")
    # a = f'{a} - {b}\n'  # Выделение только адреса ключа
    # final.write(a)
    # final.close()
    return


if __name__ == '__main__':
    pywinauto.Application().start(r'C:\DKCL\dkcl64.exe')
    cmd = f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\""
    subprocess.Popen(cmd)
    first_key()
