import subprocess
import os
import io
import pyautogui as pg
import pywinauto



def user_read(a): # Чтение папки на наличие файлов с правилами для ключей
    if os.path.exists(f'c:\DKCL\\{a}.txt'):
        read_file(a)
    else:
        a = input('Введите имя пользователя: ')
        # b = input('Введите пароль: ')pa
        user_read(a)


def open_file_address(word): # Открытие файла заполненого адресами ключей
    with io.open(f"c:\DKCL\\address.txt", encoding="utf8") as address:
        for line in address:
            if word in line:
                f = line.split('(')
                f = f[1]
                f = f.replace(")", '')
                f = f.replace("\n", '')
                f = f.replace(" ", '')
    return f


def read_file(a): # Чтение построчно файла
    with open(f"c:\DKCL\\{a}.txt", encoding="utf8") as file:  # Разбираем файл с ключами построчно
        for line in file:
            word = line.strip()
            f = open_file_address(word)
            start_dk(f)

def start_dk(f): # Запуск клиента
    subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"USE,{f}\"")
    app = pywinauto.Application().connect(title_re="DistKontrolUSB Client", class_name = "wxWindowNR")
    app.Введитепарольдляиспользованияэтогоустройства.Edit2.type_keys('12345678')
    app.Введитепарольдляиспользованияэтогоустройства.print_control_identifiers()
    app.Введитепарольдляиспользованияэтогоустройства.ЗапомнитьCheckBox.Click()
    app.Введитепарольдляиспользованияэтогоустройства.OKButton.Click()
    # app.Введитепарольдляиспользованияэтогоустройства.Запомнить.Click()
    returned_output = subprocess.check_output(f'C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys')
    c = returned_output.decode("utf-8")
    print(c)
    subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    # pg.typewrite(["enter"])
