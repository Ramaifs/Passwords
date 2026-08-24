import json, os
# Создать систему для поиска
# Сделать DRY по всем блокам функций (сделав систему поиска облегчить поиск по словарям и спискам) 
# {1 [2 {3 }3 ]2 }1 ----- [""]1 [0]2 [""]3
# Export/Import оставить напоследок
# ExistCheck добавить как один класс функций
# Сделать удаление всей программы
# Delete перенести в Edit
# Сделать систему сохранений c разными data файлов

dir_path = str(os.getenv('LOCALAPPDATA')) + "\\Ramaif Programs\\" + "PasswordManager\\"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

PathFile = dir_path + "data.json"

class System:
    data = {
        "None": [
            {"Username": "", "Email" : "", "Phone": "", "Password": ""},
            {"Username": "", "Email" : "", "Phone": "", "Password": ""}
            ]
    }
    construct = {"Username": "", "Email" : "", "Phone": "", "Password": ""}
    platform = ""
    account = 0
    option = ""

    def __init__(self, platform: str, account: int, option: str):
        self.platform = platform
        self.account = account
        self.option = option
        
    def SaveData(self):
        try:
            with open(PathFile, 'w') as file:
                json.dump(self.data, file)
        except:
            print("Не удалось сохранить нового пользователя!")

    def LoadData(self):
        with open(PathFile, 'r') as file:
            loaded_data = json.load(file)

        for name in self.data.keys():
            self.data[name] = loaded_data[name]

Loaded = False
while not Loaded:
    try:
        System.LoadData(System)
    except FileNotFoundError:
        print("Не удалось загрузить сохранение, начинаем загрузку нового сохранения..")
        System.SaveData(System)
    else:
        print("Сессия была загружена:", PathFile)
        print(System.data)
        Loaded = True

def ShowDataInfo(user: System):
    i = 0
    Names = ["None"]
    match user.platform:
        case "0":
            for name in System.data.keys():
                i += 1
                Names.append(name)
                print(f"[{i}]", name)

            print("0 - Создать новый",
                "\nExit/Quit - Выйти из выбора")
        case _:
            for acc in range( len(System.data[user.platform]) ):
                i += 1
                name = System.data[user.platform][acc]["Username"]
                print(f"Аккаунт [{i}]", name)

    return Names

def ExistCheckValues(checking, userinput: str):
    for name in checking.values():
        if str.lower(userinput) == str.lower(name):
            return True

    return False
def ExistCheckKeys(checking, userinput: str):
    for name in checking.keys():
        if str.lower(userinput) == str.lower(name):
            return True

    return False

def UsernameCreate(user: System):
    while True:
        print("\nСоздаём нового пользователя")
        UserInput = input("Имя нового пользователя: ")
        
        if ExistCheckValues(System.data[user.platform][user.account], UserInput):
            print("\nДанный пользователь уже существует!\n")
            ShowDataInfo(user)
            break
        else:
            System.data[user.platform][user.account][user.option] = UserInput
            ShowDataInfo(user)
            System.SaveData(System)
            break

while True:
    print("\nSearch - Поиск информации по всем записям",
          "\nNew - Запись нового пароля в систему",
          "\nEdit - Изменение существующего пароля в системе",
          "\nSave - Вручную сохранить данные в систему",
          "\nExport/Import - Выгрузить/Загрузить данные в другом файле",
          "\nExit/Quit - Выйти из программы")
    UserInput = str.lower(input("Что вы хотите сделать?: "))
    print()

    match UserInput:
        case "search":
            print("\nAll - Поиск по всему",
                  "\nUsername - Поиск по имени пользователя",
                  "\nEmail - Поиск по электронной почте",
                  "\nPhone - Поиск по телефону",
                  "\nPassword - Поиск по паролю")
            UserInput = str.lower(input("Выберите предпочитаемый поиск в системе: "))
            match UserInput:
                case "all":
                    pass
                case "username":
                    pass
                case "email":
                    pass
                case "phone":
                    pass
                case "password":
                    pass
        case "new":
            while True:
                user = System("0", 0, "")
                PlatformFound = False
                names = ShowDataInfo(user)

                UserInput = str.lower(input("Укажите платформу для привязки пароля: "))
                try:
                    int(UserInput)
                except:
                    match UserInput:
                        case "exit" | "quit":
                            break
                        case _:
                            if ExistCheckValues(user, UserInput):
                                user.platform = UserInput
                                PlatformFound = True
                else:
                    UserInput = int(UserInput)
                    match UserInput:
                        case i if i == 0:
                            UserInput = input("\nВыберите название для платформы: ")
                            match ExistCheckKeys(System.data, UserInput):
                                case True:
                                    print("\nДанная платформа уже существует!\n")
                                case False:
                                    System.data[UserInput] = [System.construct]
                                    System.SaveData(System)
                                    
                        case i if i == -1:
                            break
                        case i if i >= 0:
                            user.platform = names[i]
                            PlatformFound = True
                        case _:
                            print("\nУказано значение меньше нуля!\n")
                        
                    while PlatformFound:
                        print("Выбрана данная платформа:", user.platform)
                        UserInput = str.lower(input("\nУкажите аккаунт по счету: "))
                        try:
                            int(UserInput)
                        except:
                            match UserInput:
                                case "exit" | "quit":
                                    break
                                case _:
                                    print("\nВведено не числовое значение!\n")
                        else:
                            UserInput = int(UserInput)
                            if UserInput > len(System.data[user.platform]):
                                System.data[user.platform].append(System.construct)
                                user.account = len(System.data[user.platform])-1
                                print(System.data)
                            elif UserInput <= 0:
                                user.account = 0
                            else:
                                user.account = UserInput-1
                            
                            print("Выбран данный аккаунт:", user.account+1)

                            print("\nUsername - Имя пользователя",
                                "\nEmail - Электронная почта",
                                "\nPhone - Номер телефона",
                                "\nExit/Quit - Выйти из выбора")
                            UserInput = str.lower(input("Укажите к чему привязывать пароль: "))

                            match UserInput:
                                case "username":
                                    user.option = "Username"
                                    UsernameCreate(user)
                                    break
                                case "email":
                                    break
                                case "phone":
                                    break
                                case "exit" | "quit":
                                    break

                    match PlatformFound:
                        case True:
                            break
            
        case "edit":
            pass
        case "save":
            pass
        case "export":
            pass
        case "import":
            pass
        case "exit" | "quit":
            break
