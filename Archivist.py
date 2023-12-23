#Для редактирования файлов
import os, csv
import shutil
#Для бота
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject

logging.basicConfig(level=logging.INFO)

bot = Bot(token="")

dp = Dispatcher()


def l_find(l: list, elt) -> int:
    for i in range(0, len(l)):
        if l[i] == elt:
            return i
    return -1


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    ans = "Список команд:\n"
    ans += "/cf <Название папки>" + " - создаёт пустую папку" + "\n"
    ans += "/df <Номер папки>" + " - удаляет папку вместе со всем содержимым" + "\n"

    ans += "/an <Номер папки> <Запись>" + " - добавляет запись в папку" + "\n"
    ans += "/dn <Номер папки> <Номер Записи>" + " - удаляет запись из папки" + "\n"

    ans += "/slib" + " - показывает все папки в вашей библиотеке" + "\n"
    ans += "/sf <Номер папки>" + " - показывает содержимое папки" + "\n"

    ans += "/ac <Номер папки> <Номер записи> <примечание>" + " - добавляет примечание к записи" + "\n"
    ans += "/dc <Номер папки> <Номер записи> <Номер примечания>" + " - удаляет примечание к записи" + "\n"
    ans += "/dlib" + " - полностью удаляет вашу библеотеку" + "\n"
    return await message.answer(ans)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    ans = "Приветствую! Я ваш личный архивариус." + "\n"
    ans += "Я могу помочь хранить ваши записи." + "\n"
    ans += "Например вы можете создать список дел" + "\n"
    ans += "Если хотите продолжить используйте команду /clib для создания своей библиотеки" + "\n"
    return await message.answer(ans)


@dp.message(Command("clib"))
async def create_dir(message: types.Message):
    chat_id = str(message.chat.id)
    if l_find(os.listdir(os.getcwd()), chat_id) == -1:
        os.mkdir(chat_id)
        ans = "библиотека создана" + "\n"
        ans += "Используйте команду /help, если забудите команды" + "\n"
        return await message.answer(ans)
    else:
        return await message.answer("У вас уже есть своя библиотека")


@dp.message(Command("dlib"))
async def create_dir(message: types.Message):
    chat_id = str(message.chat.id)
    if l_find(os.listdir(os.getcwd()), chat_id) != -1:
        shutil.rmtree(chat_id)
        return await message.answer("Ваша библиотека удалена")
    else:
        return await message.answer("У вас нет своей библиотеки")



@dp.message(Command("an"))
async def add_note(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали парметры")
    args = command.args.split(" ", maxsplit=1)
    if len(args) < 2:
        return await message.answer("Ошибка: Вы не указали один из параметров")
    

    if args[0].isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")
    n = int(args[0])

    note = args[1]
    chat_id = str(message.chat.id)


    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Ошибка: Такой папки не существует")

    folder = l[n-1]

    with open(chat_id+"/"+folder, "a", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow([note])

    return await message.answer("Запись <" + note + "> добавлена в " + folder[:-4:])


@dp.message(Command("dn"))
async def del_note(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали параметры")
    args = command.args.split(" ", maxsplit=1)

    if len(args) < 2:
        return await message.answer("Ошибка: Вы не указали папку или номер записи")

    if args[0].isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")
    n = int(args[0])

    chat_id = str(message.chat.id)
    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Ошибка: Такой папки не существует")

    folder = l[n-1]

    if args[1].isdigit() == False:
        return await message.answer("Ошибка: Номер записи должен состоять из цифр")

    k = int(args[1])-1
    i = 0
    data = []

    with open(chat_id+"/"+folder, newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if i != k:
                data.append(row)
            i += 1

    with open(chat_id+"/"+folder, "w", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

    return await message.answer("Запись удалена успешно")


@dp.message(Command("slib"))
async def show_dir(message: types.Message):
    chat_id = str(message.chat.id)
    l = os.listdir(os.getcwd()+"/"+chat_id)
    ans = ""
    i = 1
    for t in l:
        ans += str(i) + ": " + t[:-4:] +"\n"
        i += 1
    return await message.answer(ans)


@dp.message(Command("cf"))
async def create_csv(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали название папки")

    name = command.args.split(" ", maxsplit=0)[0].lower()
    chat_id = str(message.chat.id)

    file = open(chat_id+"/"+name+".csv", 'w+')
    file.close()
    return await message.answer("Папка "+name+" создана")


@dp.message(Command("df"))
async def delete_csv(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали номер папки")


    arg = command.args.split(" ", maxsplit=1)[0]

    if arg.isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")

    n = int(arg)
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Ошибка: Такой папки не существует")
    name = l[n-1]
    os.remove(chat_id+"/"+name)
    return await message.answer("Папка "+name[:-4:]+" удалена")


@dp.message(Command("sf"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали номер папки")

    arg = command.args.split(" ", maxsplit=1)[0]

    if arg.isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")


    n = int(arg)
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n > len(l) or n < 1:
        return await message.answer("Ошибка: Такой папки не существует")

    name = l[n-1]
    name = name[:-4:]
    ans = name + ":\n"
    i = 1

    with open(chat_id+"/"+name+".csv", newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            ans += str(i) + ")"+ row[0] + "\n"
            for j in range(1, len(row)):
                ans += "Примечание "+ str(j) + ": " + row[j] +"\n"
            i += 1

    return await message.answer(ans)

@dp.message(Command("ac"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали номер папки")

    args = command.args.split(" ", maxsplit=2)
    if len(args) < 3:
        return await message.answer("Ошибка: Вы не указали один из параметров")

    if args[0].isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")
    n1 = int(args[0])

    if args[1].isdigit() == False:
        return await message.answer("Ошибка: Номер записи должен состоять из цифр")
    n2 = int(args[1])

    com = args[2]
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n1 > len(l) or n1 < 1:
        return await message.answer("Ошибка: Такой папки не существует")

    folder = l[n1-1]
    folder = folder
    i = 0
    data = []

    with open(chat_id+"/"+folder, newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
                data.append(row)

    if n2 < 0 or n2 > len(data):
        return await message.answer("Ошибка: Такой записи не существует")

    data[n2-1].append(com)

    with open(chat_id+"/"+folder, "w", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

    return await message.answer("Примечание успешно добавлено")


@dp.message(Command("dc"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Ошибка: Вы не указали номер папки")

    args = command.args.split(" ", maxsplit=3)
    if len(args) < 3:
        return await message.answer("Ошибка: Вы не указали один из параметров")

    if args[0].isdigit() == False:
        return await message.answer("Ошибка: Номер папки должен состоять из цифр")
    n1 = int(args[0])

    if args[1].isdigit() == False:
        return await message.answer("Ошибка: Номер записи должен состоять из цифр")
    n2 = int(args[1])

    if args[2].isdigit() == False:
        return await message.answer("Ошибка: Номер примечания должен состоять из цифр")
    n3 = int(args[2])

    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n1 > len(l) or n1 < 1:
        return await message.answer("Ошибка: Такой папки не существует")

    folder = l[n1-1]
    folder = folder
    i = 0
    data = []

    with open(chat_id+"/"+folder, newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
                data.append(row)

    if n2 < 0 or n2 > len(data):
        return await message.answer("Ошибка: Такой записи не существует")

    if len(data[n2-1]) == 1:
        return await message.answer("Ошибка: У этой записи нет примечания")


    if n3 < 1 or n3 > len(data[n2-1]):
        return await message.answer("Ошибка: У этой записи нет примечания с таким номером")

    data[n2-1].pop(n3-1)

    with open(chat_id+"/"+folder, "w", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

    return await message.answer("Примечание успешно удалено")

    

    


async def main():
    return await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
