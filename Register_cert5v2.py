import subprocess
import os
import io
import pywinauto
import time



def user_read():  # Чтение папки на наличие файлов с правилами для ключей
    global l
    global p
    global pin
    if os.path.exists(f'c:\DKCL\\{l}.txt'):
        check_address_file()
    else:
        l = input('Введите имя пользователя: ')
        p = input('Введите пароль для устройства: ')
        pin = input('Введите пин для ключей: ')
        user_read()


def check_address_file():
    with open(f'c:\DKCL\\keys.txt', encoding='Utf8') as key:
        kf = key.read()

    with open(f"c:\DKCL\\{l}.txt", encoding="utf8") as address:
        for needle in (line.strip() for line in address):
            if needle not in kf:
                print(needle, 'Адрес не найден. Поправьте файл пользователя')
                programName = "notepad.exe"
                fileName = f"c:\DKCL\\{l}.txt"
                subprocess.check_output([programName, fileName])
    read_file()


def read_file():  # Чтение построчно файла
    with open(f"c:\DKCL\\{l}.txt", 'r', encoding="utf8") as file:  # Разбираем файл с ключами построчно
        for line in file:
            word = line.strip()
            f = open_file_address(word)
            start_dk(f, word)


def open_file_address(word):  # Открытие файла заполненого адресами ключей
    with io.open(f"c:\DKCL\\keys.txt", encoding="utf8") as address:
        for line in address:
            if word in line:
                f = line.split('(')
                f = f[1]
                f = f.replace(")", '')
                f = f.replace("\n", '')
                f = f.replace(" ", '')
    return f


def start_dk(f, word):  # Запуск клиента
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"USE,{f}\"")
    time.sleep(5)
    # Проверка на сохраненный пароль
    cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys1.txt"
    subprocess.run(cmd)
    b = open(f"c:\DKCL\\keys1.txt", "r", encoding="utf8", )
    b_read = b.readlines()
    for line in b_read:
        if f in line:
            # subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"")
            print(line)
            if line.count('In-use by you') > 0:
                cripto_pro()
            else:
                if line.count('In-use by:') > 0:
                    print(f"Порт занят. Данный адрес будет удален {word}, а я пока продолжу работу")
                    del_str(word)
                else:
                    client_dkcl_input()


def del_str(word):  # Удаление адреса из файла
    with open(f"c:\DKCL\\{l}.txt", 'r+', encoding="utf8") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if word not in i:
                f.write(i)
        f.truncate()
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"")
    read_file()


def client_dkcl_input():
    # Вернуть Временно
    app = pywinauto.Application().connect(title_re="DistKontrolUSB Client", class_name="wxWindowNR")
    app.Введитепарольдляиспользованияэтогоустройства.Edit.type_keys(f'{l}')
    app.Введитепарольдляиспользованияэтогоустройства.Edit2.type_keys(f'{p}')
    # app.DistKontrolUSB.print_control_identifiers() # Вывод параметров формы
    app.Введитепарольдляиспользованияэтогоустройства.ЗапомнитьCheckBox.click()
    app.Введитепарольдляиспользованияэтогоустройства.OKButton.click()
    time.sleep(2)
    cripto_pro()
    return


def cripto_pro():  # запуск крипто получение списка ключей
    cmd = "C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys"
    returned_output = subprocess.check_output(cmd)
    b = returned_output.decode("utf-8")
    start = -1
    count = 0
    # print(b) # Список ключей

    while True:
        start = b.find("Aladdin R.D. JaCarta", start + 1)
        # d = b.split('Aladdin R.D. JaCarta ')
        # print(d)
        if start == -1:
            break
        count += 1

    b = b.split('Aladdin R.D. JaCarta 0')

    i = 1
    d = []
    while i <= count:
        e = b[i]
        # print(e)
        if e.find('1FFFF\\') > 0:
            e = e.replace('1FFFF\\', '')
            e = e.partition('\r')[0]
            # print(e)
        else:
            e = e.partition('\r')[0]
            e = e.replace('\\','')
            # print(e)
        # d += [e]
        print(e)
        i += 1

        # for el in d:
        #     el = el.replace('\r', '')
        #     print(el)
        #     subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest.exe -property -cinstall -cont {el}')
        #     time.sleep(1)
        #     subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -delsaved -container {el}')
        #     time.sleep(1)
        #     subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -check -cont {el}')
        #     time.sleep(30)


        subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest.exe -property -cinstall -cont {e}')
        time.sleep(1)
        subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -delsaved -container {e}')
        time.sleep(1)
        subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -check -cont {e}')
        time.sleep(30)
        try:
            app = pywinauto.Application().connect(title_re="Аутентификация - КриптоПро CSP", class_name="#32770")
        except pywinauto.ElementNotFoundError:
            time.sleep(30)
            app = pywinauto.Application().connect(title_re="Аутентификация - КриптоПро CSP", class_name="#32770")
            app.АутентификацияКриптоПроCSP.Edit.type_keys(f'{pin}')
            app.АутентификацияКриптоПроCSP.СохранитьпарольвсистемеCheckBox.click()
            app.АутентификацияКриптоПроCSP.OKButton.click()
        else:
            # app.АутентификацияКриптоПроCSP.print_control_identifiers()
            app.АутентификацияКриптоПроCSP.Edit.type_keys(f'{pin}')
            app.АутентификацияКриптоПроCSP.СохранитьпарольвсистемеCheckBox.click()
            app.АутентификацияКриптоПроCSP.OKButton.click()
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"")
    return

    # cmd = "C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys"
    # returned_output = subprocess.check_output(cmd)
    # b = returned_output.decode("utf-8")
    # print(b)
    # b = b.split(' ')
    # b = b[14]
    # b = b.replace('0\\', '')
    # b = b.replace('\r\nOK.\r\nTotal:', '')  # Вытаскиваем ид ключа
    # # csptest.exe - property - cinstall - cont
    # subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest.exe -property -cinstall -cont {b}')
    # time.sleep(1)
    # subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -delsaved -container {b}')
    # time.sleep(1)
    # subprocess.Popen(f'C:\Program Files\Crypto Pro\CSP\csptest -passwd -check -cont {b}')
    # time.sleep(15)
    # app = pywinauto.Application().connect(title_re="Аутентификация - КриптоПро CSP", class_name="#32770")
    # # app.АутентификацияКриптоПроCSP.print_control_identifiers()
    # app.АутентификацияКриптоПроCSP.Edit.type_keys(f'{pin}')
    # app.АутентификацияКриптоПроCSP.СохранитьпарольвсистемеCheckBox.click()
    # app.АутентификацияКриптоПроCSP.OKButton.click()
    # subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"")
    # return


if __name__ == '__main__':
    print('Проверить наличие файла с названием логин.txt в папке DKCL')
    l = input('Введите логин для устройства: ')
    p = input('Введите пароль для устройства: ')
    pin = input('Введите пин для ключей: ')
    app = pywinauto.Application().start(r'C:\DKCL\dkcl64.exe')
    subprocess.Popen(f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\"")
    user_read()
