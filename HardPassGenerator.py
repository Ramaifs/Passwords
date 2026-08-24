# Это последняя версия моей программы PasswordGenerator

import random, json, os, pyperclip
from collections import Counter

Lower = "abcdefghijklmnopqrstuvwxyz"
Upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Numbers = "1234567890"
Symbols = "~`!@#$%^&*()-_+=:;'?/,."

All = [Lower, Upper, Numbers, Numbers, Upper, Lower]
AllPossible = (Symbols, Lower, Upper, Numbers)

PasswordLen = 20
RepeatPassword = 10

ClipboardPasswords = []

dir_path = str(os.getenv('LOCALAPPDATA')) + "\\Ramaif Programs\\" + "HardPassGenerator\\"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

PathFile = dir_path + "data.json"

SummarizeString = ""

def SummarizeFunc(SummaryCount):
    global SummarizePasswords, SummarizeString
    letter_counts = Counter(SummarizeString)
    top_letters = letter_counts.most_common(SummaryCount)
    for letter, count in top_letters:
        print(f'\'{letter}\': {count} раз(а)')
    print(f"Всего символов в паролях было: {len(SummarizeString)}")

def PasswordSettings():
    global PasswordLen, RepeatPassword, All
    PasswordLen = input("Какой длины будет пароль? (Цифра/Число): ")
    while True:
        try:
            PasswordLen = int(PasswordLen)
        except:
            PasswordLen = input("Введено не Number(s), какой длины будет пароль? (Цифра/Число): ")
        else:
            break

    RepeatPassword = input("Сколько за один раз сгенерировать паролей? (Цифра/Число): ")
    while True:
        try:
            RepeatPassword = int(RepeatPassword)
        except:
            RepeatPassword = input("Введено не Number(s), сколько за один раз сгенерировать паролей? (Цифра/Число): ")
        else:
            if RepeatPassword > 0:
                break
            elif RepeatPassword <= 0:
                RepeatPassword = 1
                break
    
    if str.lower(input("Изменить принцип подбора паролей? (Y/N): ")) == "y":
        print("\n Текущая генерация такая:")
        for i in range(0, len(All)):
            print(str(i) + ". " + All[i])
        print("\n Все возможные генерации:")
        for i in range(0, len(AllPossible)):
            print(str(i) + ". " + AllPossible[i])
        Changed = ""
        iterator = 0
        AllNew = []
        AlcorithmCount = 8
        while True:
            AlcorithmCount = input("Сколько разных символических/буквенных подборов использовать в пароле? (Цифра/Число): ")
            try:
                AlcorithmCount = int(AlcorithmCount)
            except:
                print("Введено не Number(s), сколько разных символических/буквенных подборов использовать в пароле? (Цифра/Число): ")
            else:
                break
        for i in range(0, AlcorithmCount):
            list.insert(AllNew, i, "")
        print("\n Введите " + str(AlcorithmCount) + " подборов, цифрами от 0 до 3 (В скобках лежит значение по умолчанию)")
        print("\n Начало изменения генерации паролей..")
        while True:
            if iterator > AlcorithmCount-1:
                All = AllNew
                print("Новая генерация такая:")
                for i in range(0, len(All)):
                    print(str(i) + ". " + All[i])
                break
            
            if iterator < len(All):
                Changed = input(str(iterator + 1) + ". (" + All[iterator] + ") введите цифру из \"Все возможные генерации\": ")
            else:
                Changed = input(str(iterator + 1) + ". (" + "Новое" + ") введите цифру из \"Все возможные генерации\": ")
            try:
                Changed = int(Changed)
            except:
                print("Введён не Number, введите цифру от 0 до 3")
            else:
                if Changed > 3:
                    print("Введена цифра/число больше 3, введите цифру от 0 до 3")
                elif Changed < 0:
                    print("Введена цифра/число меньше 0, введите цифру от 0 до 3")
                else:
                    if iterator < len(All):
                        print("Значение " + All[iterator] + " изменено на " + AllPossible[Changed])
                    else:
                        print("Новое значение " + AllPossible[Changed] + " было добавлено")
                    AllNew[iterator] = AllPossible[Changed]
                    iterator += 1

def RestoreDefaultSettings():
    data = {
        "All": [Symbols, Lower, Upper, Numbers, Numbers, Upper, Lower, Symbols],
        "PasswordLen": 20,
        "RepeatPassword": 10
    }

    with open(PathFile, 'w') as file:
        json.dump(data, file)

    LoadData()

def LoadData():
    global All, PasswordLen, RepeatPassword
    with open(PathFile, 'r') as file:
        loaded_data = json.load(file)
        
    All = loaded_data["All"]
    PasswordLen = loaded_data["PasswordLen"]
    RepeatPassword = loaded_data["RepeatPassword"]

def SaveData():
    data = {
        "All": All,
        "PasswordLen": PasswordLen,
        "RepeatPassword": RepeatPassword
    }

    with open(PathFile, 'w') as file:
        json.dump(data, file)

try:
    LoadData()
except FileNotFoundError:
    print("Не удалось загрузить сохранение")
else:
    print("Прошлая сессия была загружена")

while True:
    GeneratePassword = str.lower(input("Сгенерировать пароль(и)? (Y/N/Num): "))
    if GeneratePassword == "y":
        list.clear(ClipboardPasswords)
        for r in range(0, RepeatPassword): # type: ignore
            Password = ""
            for i in range(0, PasswordLen): # type: ignore
                Random = ""
                RandomNum = random.randrange(1, len(All))
                iterator = 0
                for x in All:
                    iterator += 1
                    if iterator == RandomNum:
                        Random = x

                Direct = ""
                DirectNum = random.randrange(1, len(Random))
                iterator = 0
                for y in Random:
                    iterator += 1
                    if iterator == DirectNum:
                        Direct = y
                
                Password = Password + Direct

            UnicodeTable = []
            for char in Password:
                list.insert(UnicodeTable, len(UnicodeTable), ord(char))
            Password = ""

            for uni in UnicodeTable:
                Encrypt = random.randrange(0, 11)
                if random.randrange(0, 2) == 1:
                    Encrypt = -Encrypt

                Password += chr(uni+Encrypt)

            list.insert(ClipboardPasswords, -1, Password)
            SummarizeString += Password
            print(str(r + 1) + ": " + Password)

    elif GeneratePassword == "/cmds":
        while True:
            Command = str.lower(input("Введите команду: "))
            if Command == "help":
                print("Список доступных команд: ",
                       "\n 1. Summarize / Leader - Выводит самое повторяемый символ из сгенерированных паролей", 
                       "\n 2. Settings / SPass - Изменение параметров пароля", 
                       "\n 3. Exit / Quit - Сохраняет изменения и выходит из программы", 
                       "\n 4. GeneratePassword / GPass - Меню загрузки пароля",
                       "\n 5. RestoreSettings / RS - Возвращает все значения по умолчанию",
                       "\n 6. LocalData / LC - Открыть папку с сохранёнными данными приложения"
                      )
            elif Command == "summarize" or Command == "leader":
                if str.lower(input("Суммаризировать какие символы/буквы больше всего использовались в пароле? (Y/N): ")) == "y":
                    SummaryCount = input("Сколько показано будет символов/букв которые чаще всего использовались? (Цифра/Число): ")
                    while True:
                        try:
                            SummaryCount = int(SummaryCount)
                        except:
                            SummaryCount = input("Введено не Number(s), сколько символов/букв будет в топе? (Цифра/Число): ")
                        else:
                            if SummaryCount > 0:
                                break
                            else:
                                input("Введена цифра/число меньше 1, введите число или цифру больше или равной 1")

                    SummarizeFunc(SummaryCount)
            elif Command == "settings" or Command == "spass":
                if str.lower(input("Вы хотите изменить параметры паролей? (Y/N): ")) == "y":
                    PasswordSettings()
            elif Command == "quit" or Command == "exit":
                if str.lower(input("Выйти из программы? (Y/N): ")) == "y":
                    break
            elif Command == "generatepassword" or Command == "gpass":
                SummarizeString = ""
                break
            elif Command == "restoresettings" or Command == "rs":
                if str.lower(input("Вы уверены что хотите вернуть все настройки по умолчанию? (Y/N): ")) == "y":
                    RestoreDefaultSettings()
            elif Command == "localdata" or Command == "lc":
                os.startfile(dir_path)
        
        if Command == "quit" or Command == "exit":
            SaveData()
            break
    elif GeneratePassword == "n":
        if str.lower(input("Выйти из программы? (Y/N): ")) == "y":
            SaveData()
            break

    else:
        while True:
            try:
                GeneratePassword = int(GeneratePassword)
            except Exception:
                break
            else:
                if GeneratePassword <= RepeatPassword and len(ClipboardPasswords) > 0:
                    pyperclip.copy(ClipboardPasswords[GeneratePassword-2])
                    print(f"Пароль '{ClipboardPasswords[GeneratePassword-2]}' скопирован в буфер обмена!")
                    break
                else:
                    break
        