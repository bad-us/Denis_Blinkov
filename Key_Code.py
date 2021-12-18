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


def write_file():
    cmd = "C:\DKCL\dkcl64.exe -t \"LIST\" -r=c:\DKCL\\keys.txt"  # Здесь вместо date Ваша команда для git
    returned_output = subprocess.check_output(cmd)  # returned_output содержит вывод в виде строки байтов
    print('Сохранение в файл:', returned_output.decode("utf-8"))  # Преобразуем байты в строку
    first_key()

def write_new_file(fk):
    if fk == '2':  # Создаем файл в зависимости от ключа
        fn = 'fqcn'
    else:
        fn = 'jacarta'
    final = open(f"c:\DKCL\\Final_file_{fn}.txt", "w", encoding="utf8")
    final.close()
    return fk

def read_file(fk):
    word = "-->"
    fk = write_new_file(fk)
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
                    b = fqcn_address(f)
                else:
                    b = jacarta_address(f)
                write_final_file(a, b, fk)
    return


def fqcn_address(f):
    cmd = f"C:\DKCL\dkcl64.exe -t \"USE,{f}12345678\""  # 12345678 пароль пользователя
    subprocess.run(cmd)
    time.sleep(5)
    # Забираем UID ключа полный
    cmd = "C:\Program Files\Crypto Pro\CSP\csptest.exe -keyset -enum_cont -verifycontext -fqcn -machinekeys"
    returned_output = subprocess.check_output(cmd)
    b = returned_output.decode("utf-8")
    b = b.split(' ')
    b = b[14]
    b = b.replace('\r\nOK.\r\nTotal:', '')  # Вытаскиваем ид ключа
    # subprocess.check_output(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    time.sleep(3)
    return b


def jacarta_address(f):
    cmd = f"C:\DKCL\dkcl64.exe -t \"USE,{f}12345678\""  # 12345678 пароль пользователя
    # subprocess.check_output(cmd)
    subprocess.run(cmd)
    time.sleep(5)
    # Забираем наименование Jacarta
    cmd = "C:\Program Files\Crypto Pro\CSP\csptest -keyset -enum_cont -verifycontext -uniq"  # bad
    returned_output = subprocess.check_output(cmd)
    b = returned_output.decode("utf-8")
    b = b.split('|SCARD')
    b = b[1]
    b = b.split('\\')
    b = b[1]
    subprocess.run(f"C:\DKCL\dkcl64.exe -t \"STOP USING,{f}\"")
    time.sleep(3)
    return b


def write_final_file(a, b, fk):
    if fk == '2':
        final = open(f"c:\DKCL\\Final_file_fqcn.txt", "a", encoding="utf8")
    else:
        final = open(f"c:\DKCL\\Final_file_jacarta.txt", "a", encoding="utf8")
    # final = open(f"c:\DKCL\\Final_file_{fk}.txt", "a", encoding="utf8")
    # b = b.replace('JACARTA_', '')
    a = f'{a} - {b}\n'  # Выделение только адреса ключа
    final.write(a)
    final.close()
    return


if __name__ == '__main__':
    pywinauto.Application().Start(r'C:\DKCL\dkcl64.exe')
    cmd = f"C:\DKCL\dkcl64.exe -t \"STOP USING ALL\""
    subprocess.Popen(cmd)
    first_key()
