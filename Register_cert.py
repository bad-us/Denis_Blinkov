import subprocess
import os
import io
import re
import pywinauto

def check_address_file(l, p):
    with open(f'c:\DKCL\\keys.txt', encoding='Utf8') as key:
        kf = key.read()

    with open(f"c:\DKCL\\{l}.txt", encoding="utf8") as address:
        for needle in (line.strip() for line in address):
            if needle not in kf:
                print(needle, 'Адрес не найден. Поправьте файл пользователя')
    programName = "notepad.exe"
    fileName = f"c:\DKCL\\{l}.txt"
    subprocess.check_output([programName, fileName])
    read_file(l, p)


def user_read(l, p):  # Чтение папки на наличие файлов с правилами для ключей
    if os.path.exists(f'c:\DKCL\\{l}.txt'):
        check_address_file(l, p)
    else:
        l = input('Введите имя пользователя: ')
        p = input('Введите пароль для устройства: ')
        user_read(l, p)


def open_file_address(l, p, word):  # Открытие файла заполненого адресами ключей
    with io.open(f"c:\DKCL\\keys.txt", encoding="utf8") as address:
        for line in address:
            if word in line:
                f = line.split('(')
                f = f[1]
                f = f.replace(")", '')
                f = f.replace("\n", '')
                f = f.replace(" ", '')
    return f


def del_str(l, p, word):  # Удаление адреса из файла
    with open(f"c:\DKCL\\{l}.txt", 'r+', encoding="utf8") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if word not in i:
                f.write(i)
        f.truncate()
    read_file(l, p)


def read_file(l, p):  # Чтение построчно файла
    with open(f"c:\DKCL\\{l}.txt", 'r', encoding="utf8") as file:  # Разбираем файл с ключами построчно
        for line in file:
            word = line.strip()
            f = open_file_address(l, p, word)
            start_dk(f, l, p, word)


def start_dk(f, l, p, word):  # Запуск клиента
    subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"USE,{f}\"")
    # Проверка на сохраненный пароль
    cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys1.txt"
    subprocess.run(cmd)
    b = open(f"c:\DKCL\\keys1.txt", "r", encoding="utf8", )
    b_read = b.readlines()
    for line in b_read:
        if f in line:
            print(line)
            if line.count('In-use') > 0:
                print(f"Порт занят. Данный адрес будет удален {word}\n, а я пока продолжу работу")
                del_str(l, p, word)
                # read_file(l, p)
            else:
                print("No")
    # Вернуть Временно
    # app = pywinauto.Application().connect(title_re="DistKontrolUSB Client", class_name = "wxWindowNR")
    # app.Введитепарольдляиспользованияэтогоустройства.Edit.type_keys(f'{l}')
    # app.Введитепарольдляиспользованияэтогоустройства.Edit2.type_keys(f'{p}')
    # app.DistKontrolUSB.print_control_identifiers()
    # app.Введитепарольдляиспользованияэтогоустройства.print_control_identifiers()
    # app.Введитепарольдляиспользованияэтогоустройства.ЗапомнитьCheckBox.Click()
    # app.Введитепарольдляиспользованияэтогоустройства.OKButton.Click()
    # # app.Введитепарольдляиспользованияэтогоустройства.Запомнить.Click()
    # returned_output = subprocess.check_output(f'C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys')
    # c = returned_output.decode("utf-8")
    # print(c)
    # subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    # pg.typewrite(["enter"])


if __name__ == '__main__':
    l = input('Введите логин для устройства: ')
    p = input('Введите пароль для устройства: ')
    app = pywinauto.Application().Start(r'C:\DKCL\dkcl64.exe')
    # subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"") # Вернуть Временно
    user_read(l, p)

