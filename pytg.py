#coding=windows-1251

#Äëÿ ñîçäàíèÿ ôàéëîâ
import os, csv
import shutil
#Äëÿ áîòà
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject

logging.basicConfig(level=logging.INFO)

bot = Bot(token="TOKEN")

dp = Dispatcher()


def l_find(l: list, elt) -> int:
    for i in range(0, len(l)):
        if l[i] == elt:
            return i
    return -1


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    ans = "Ñïèñîê êîìàíä:\n"
    ans += "/cf <Íàçâàíèå ïàïêè>" + " - ñîçäà¸ò ïóñòóþ ïàïêó" + "\n"
    ans += "/df <Íîìåð ïàïêè>" + " - óäàëÿåò ïàïêó âìåñòå ñî âñåì ñîäåðæèìûì" + "\n"

    ans += "/an <Íîìåð ïàïêè> <Çàïèñü>" + " - äîáàâëÿåò çàïèñü â ïàïêó" + "\n"
    ans += "/dn <Íîìåð ïàïêè> <Íîìåð Çàïèñè>" + " - óäàëÿåò çàïèñü èç ïàïêè" + "\n"

    ans += "/slib" + " - ïîêàçûâàåò âñå ïàïêè â âàøåé áèáëèîòåêå" + "\n"
    ans += "/sf <Íîìåð ïàïêè>" + " - ïîêàçûâàåò ñîäåðæèìîå ïàïêè" + "\n"

    ans += "/ac <Íîìåð ïàïêè> <Íîìåð çàïèñè> <ïðèìå÷àíèå>" + " - äîáàâëÿåò ïðèìå÷àíèå ê çàïèñè" + "\n"
    ans += "/dc <Íîìåð ïàïêè> <Íîìåð çàïèñè> <Íîìåð ïðèìå÷àíèÿ>" + " - óäàëÿåò ïðèìå÷àíèå ê çàïèñè" + "\n"
    ans += "/dlib" + " - ïîëíîñòüþ óäàëÿåò âàøó áèáëåîòåêó" + "\n"
    return await message.answer(ans)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    ans = "Ïðèâåòñòâóþ! ß âàø ëè÷íûé àðõèâàðèóñ." + "\n"
    ans += "ß ìîãó ïîìî÷ü õðàíèòü âàøè çàïèñè." + "\n"
    ans += "Íàïðèìåð âû ìîæåòå ñîçäàòü ñïèñîê äåë" + "\n"
    ans += "Åñëè õîòèòå ïðîäîëæèòü èñïîëüçóéòå êîìàíäó /clib äëÿ ñîçäàíèÿ ñâîåé áèáëèîòåêè" + "\n"
    return await message.answer(ans)


@dp.message(Command("clib"))
async def create_dir(message: types.Message):
    chat_id = str(message.chat.id)
    if l_find(os.listdir(os.getcwd()), chat_id) == -1:
        os.mkdir(chat_id)
        ans = "áèáëèîòåêà ñîçäàíà" + "\n"
        ans += "Èñïîëüçóéòå êîìàíäó /help, åñëè çàáóäèòå êîìàíäû" + "\n"
        return await message.answer(ans)
    else:
        return await message.answer("Ó âàñ óæå åñòü ñâîÿ áèáëèîòåêà")


@dp.message(Command("dlib"))
async def create_dir(message: types.Message):
    chat_id = str(message.chat.id)
    if l_find(os.listdir(os.getcwd()), chat_id) != -1:
        shutil.rmtree(chat_id)
        return await message.answer("Âàøà áèáëèîòåêà óäàëåíà")
    else:
        return await message.answer("Ó âàñ íåò ñâîåé áèáëèîòåêè")



@dp.message(Command("an"))
async def add_note(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè ïàðìåòðû")
    args = command.args.split(" ", maxsplit=1)
    if len(args) < 2:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè îäèí èç ïàðàìåòðîâ")
    
    n = int(args[0])

    note = args[1]
    chat_id = str(message.chat.id)


    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")

    folder = l[n-1]

    with open(chat_id+"/"+folder, "a", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow([note])

    return await message.answer("Çàïèñü <" + note + "> äîáàâëåíà â " + folder[:-4:])


@dp.message(Command("dn"))
async def del_note(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè ïàðàìåòðû")
    args = command.args.split(" ", maxsplit=1)

    if len(args) < 2:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè ïàïêó èëè íîìåð çàïèñè")


    n = int(args[0])
    chat_id = str(message.chat.id)
    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")

    folder = l[n-1]
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

    return await message.answer("Çàïèñü óäàëåíà óñïåøíî")


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
        return await message.answer("Îøèáêà: Âû íå óêàçàëè íàçâàíèå ïàïêè")

    name = command.args.split(" ", maxsplit=1)[0].lower()
    chat_id = str(message.chat.id)

    file = open(chat_id+"/"+name+".csv", 'w+')
    file.close()
    return await message.answer("Ïàïêà "+name+" ñîçäàíà")


@dp.message(Command("df"))
async def delete_csv(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè íîìåð ïàïêè")

    n = int(command.args.split(" ", maxsplit=1)[0])
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)

    if n > len(l) or n < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")
    name = l[n-1]
    os.remove(chat_id+"/"+name)
    return await message.answer("Ïàïêà "+name[:-4:]+" óäàëåíà")


@dp.message(Command("sf"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè íîìåð ïàïêè")

    n = int(command.args.split(" ", maxsplit=1)[0])
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n > len(l) or n < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")

    name = l[n-1]
    name = name[:-4:]
    ans = name + ":\n"
    i = 1

    with open(chat_id+"/"+name+".csv", newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            ans += str(i) + ")"+ row[0] + "\n"
            for j in range(1, len(row)):
                ans += "Ïðèìå÷àíèå "+ str(j) + ": " + row[j] +"\n"
            i += 1

    return await message.answer(ans)

@dp.message(Command("ac"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè íîìåð ïàïêè")

    args = command.args.split(" ", maxsplit=2)
    if len(args) < 3:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè îäèí èç ïàðàìåòðîâ")

    n1 = int(args[0])
    n2 = int(args[1])
    com = args[2]
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n1 > len(l) or n1 < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")

    folder = l[n1-1]
    folder = folder
    i = 0
    data = []

    with open(chat_id+"/"+folder, newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
                data.append(row)

    if n2 < 0 or n2 > len(data):
        return await message.answer("Îøèáêà: Òàêîé çàïèñè íå ñóùåñòâóåò")

    data[n2-1].append(com)

    with open(chat_id+"/"+folder, "w", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

    return await message.answer("Ïðèìå÷àíèå óñïåøíî äîáàâëåíî")


@dp.message(Command("dc"))
async def show_folder(message: types.Message, command: CommandObject):
    if command.args is None:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè íîìåð ïàïêè")

    args = command.args.split(" ", maxsplit=3)
    if len(args) < 3:
        return await message.answer("Îøèáêà: Âû íå óêàçàëè îäèí èç ïàðàìåòðîâ")

    n1 = int(args[0])
    n2 = int(args[1])
    n3 = int(args[2])
    chat_id = str(message.chat.id)

    l = os.listdir(os.getcwd() + "/" + chat_id)
    if n1 > len(l) or n1 < 1:
        return await message.answer("Îøèáêà: Òàêîé ïàïêè íå ñóùåñòâóåò")

    folder = l[n1-1]
    folder = folder
    i = 0
    data = []

    with open(chat_id+"/"+folder, newline='', encoding = "utf-8") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
                data.append(row)

    if n2 < 0 or n2 > len(data):
        return await message.answer("Îøèáêà: Òàêîé çàïèñè íå ñóùåñòâóåò")

    if len(data[n2-1]) == 1:
        return await message.answer("Îøèáêà: Ó ýòîé çàïèñè íåò ïðèìå÷àíèÿ")


    if n3 < 1 or n3 > len(data[n2-1]):
        return await message.answer("Îøèáêà: Ó ýòîé çàïèñè íåò ïðèìå÷àíèÿ ñ òàêèì íîìåðîì")

    data[n2-1].pop(n3-1)

    with open(chat_id+"/"+folder, "w", newline='', encoding = "utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(data)

    return await message.answer("Ïðèìå÷àíèå óñïåøíî óäàëåíî")

    

    


async def main():
    return await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
