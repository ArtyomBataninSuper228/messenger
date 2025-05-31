import sys
import dearpygui.dearpygui as dpg #импорт графического модуля
import  requests
#from requests_toolbelt import MultipartEncoder
from threading import Thread # импорт многопоточности
import time
import datetime# импорт модуля отвечающего за время
import os
#import sounddevice as sound_device
#import soundfile as sound_file
import simpleaudio as simple_audio #импорт звукового модуля
import subprocess# импорт модуля, открывающего файлы
import mycode as code
import json




imges = []
is_coding = True
pth = os.path.dirname(os.path.abspath(__file__))

def path2(p):
    new_path = pth + "/files/" + p
    return new_path

key = code.key()
key.open_key_from_file(path2("key.k"))

def clear_Images_data():
    for i in os.listdir(pth + "/download/" + "Images"):
        os.remove(pth + "/download/" + "Images/" + i)
    for i in os.listdir(path2("coded")):
        os.remove(path2("coded/") + i)
clear_Images_data()
class addresses: # читаем и приводим в порядок данные из адрессной книги
    def __init__(self, Name, Address):
        self.addres = Address
        self.name = Name
try:

    data_file = open(path2("data.txt"), mode="r")
    data = []
except:
    print("Отсутствует файл настройки. Переустановите клиент.")
    time.sleep(5)
    sys.exit()
for i in data_file.readlines():
    data.append(i[:-1])
data_file.close()
try:
    address_book_file = open(path2("Address_book.txt"), mode="r")
    address_book = address_book_file.readlines()
    address_book_file.close()
except:
    f = open(path2("Address_book.txt"), mode="W")
    f.close()
    address_book_file = open(path2("Address_book.txt"), mode="r")
    address_book = address_book_file.readlines()
    address_book_file.close()

def download_file_address(name):
    if data[14] == "None":
        new_path = pth + "/download/" + name
        return new_path
    else:
        new_path = os.path.join(data[14], name)
        return new_path
def sound():
    if data[13] == "True":
        filename = path2("747-400 gwrn.wav")
        wave_object = simple_audio.WaveObject.from_wave_file(filename)

        #play_object = wave_object.play()
        #play_object.wait_done()

def sound_error():
    if data[13] == "True":
        filename = path2("error 4.wav")
        wave_object = simple_audio.WaveObject.from_wave_file(filename)
        #play_object = wave_object.play()
        #play_object.wait_done()


address_book2 = []
num = 0
while num < len(address_book)-1:
    name = str(address_book[num])[:-1]
    num += 1
    address = str(address_book[num])[:-1]
    num += 1
    obj = addresses(name, address)
    address_book2.append(obj)
chats_data = {}
is_connect = {"now":False, "time":{}, "num":{}}
for i in address_book2:
    is_connect["time"][i.addres] = []




def update_chat(chat):
        time_of_previos_update = 0
        connect = False
        while is_run:
            try:
                c = code.code()
                c.key = key
                c.bytes = bytes(chat.addres, "utf-8")
                c.coding_with_open_key()
                coded_tm = requests.get(data[15] + "get_chat_time", json={"chat": json.dumps(c.koded)}).json()["time"]
                c.koded = json.loads(coded_tm)
                c.decoding_with_open_key()
                tim = float(c.bytes.decode("utf-8"))
                if time_of_previos_update < tim:
                    t1 = float(time.time())
                    # chats_data[chat.addres] = requests.get(data[2], json={"chat": chat.addres}).json()["chat"]
                    raw_chat = requests.get(data[15] + "get_chat_with_coding", json={"chat": chat.addres}).json()[
                        "chat"]
                    t2 = float(time.time())
                    t3 = t2 - t1
                    connect = True
                    ch = []
                    c.koded = json.loads(raw_chat)
                    c.decoding_with_open_key()
                    decoded_chat = json.loads(c.bytes.decode("utf-8"))
                    nm = 0
                    for message in decoded_chat:
                        if message[0] == "Text":
                            text = Text(message[1], message[2], chat, message[3], nm, message[4])
                            ch.append(text)
                        elif message[0] == "Sound":
                            snd = Sounds(message[1], message[2], chat, message[3], nm, message[4])
                            ch.append(snd)
                        elif message[0] == "Images":
                            pass
                            #im = Images(message[1], message[2], chat, nm, nm, message[4])
                        nm += 1



                    is_connect["time"][chat.addres].append(t3)
                    chats_data[chat.addres] = ch
                    while len(is_connect["time"][chat.addres]) > 41:
                        is_connect["time"][chat.addres].pop(0)
                    is_connect["num"][chat.addres] = []
                    for i in range(0, len(is_connect["time"][chat.addres])):
                        is_connect["num"][chat.addres].append(i)
                    coded_tm = requests.get(data[15] + "get_time_2").json()["time"]
                    c.koded = json.loads(coded_tm)
                    c.decoding_with_open_key()
                    time_of_previos_update = float(c.bytes.decode("utf-8"))


            except ZeroDivisionError:
                connect = False
            is_connect["now"] = connect
            time.sleep(1)
ths = []
def update_data_messages():
    n = 0
    for i in address_book2:
        ths.append( Thread(target=update_chat, args=(i, )))
        ths[n].start()
        n += 1








is_run = True
t1 = Thread(target=update_data_messages)
t1.start()

def write_to_file():
    file = open(path2("Address_book.txt"), mode="w")
    for i in address_book2:
        print(i.name, file=file)
        print(i.addres, file=file)

    file.close()
#json={"chat": chataddress, "body": ("Text", time_now, data[0], text, files_names)} структура сообщения

#Классы сообщений
class Messages:
    time = None
    sender = None
    chat = None
    num = None

    def __init__(self, time, sender, chat, num):
        self.time = time
        self.sender = sender
        self.chat = chat
        self.num = num


class Sounds(Messages):
    hears = []
    visions = []

    def __init__(self, time, sender, chat, hears, num, visions):
        super(Sounds, self).__init__(time, sender, chat, num)
        self.hears = hears
        self.visions = visions

    def sound(self):
        if data[0] in self.visions:
            pass
        else:
            self.visions.append(data[0])
            requests.get(data[4], json={"chat": self.chat, "num": self.num,
                                        "body": ["Sound", self.time, self.sender, self.hears, self.visions]})
        if data[0] not in self.hears:

            t9 = Thread(target=sound)
            t9.start()
            if data[13] == "True":
                self.hears.append(data[0])
                requests.get(data[4], json={"chat": self.chat, "num": self.num, "body": ["Sound", self.time, self.sender, self.hears, self.visions]})

    def send(self):
        try:

            with dpg.window(label="Отправка файлов", height=200, width=400, no_close=True):
                tag = dpg.last_item()
                with dpg.child_window():
                    dpg.add_text("Отправка сообщения", color=(25, 255, 50))

                time_now = str(datetime.datetime.now())
                c = code.code()
                c.key = key
                body = {"chat": self.chat, "body": ["Sound", self.time, self.sender, self.hears, self.visions]}
                jsn = json.dumps(body)
                c.bytes = bytes(jsn, "utf-8")
                c.coding_with_open_key()
                requests.get(data[15] + "send_with_coding", json=json.dumps(c.koded))
                dpg.delete_item(tag)
        except:
            dpg.delete_item(tag)
            error_connect()
    def delete(self):
        requests.get(data[7], json={"chat": self.chat, "time": self.time, "sender": self.sender, "num": self.num, "files": self.hears, "type":"Sound", "visions": self.visions})



class Images(Messages):
    image_address = None
    image_data = None
    name = None
    tag = None
    had_downloaded = False
    def __init__(self, time, sender, chat, num, name, image_address):
        super(Images, self).__init__(time, sender, chat, num)
        self.name = name
        self.image_address = image_address
    def send(self):
        #file = open(self.image_address, mode = "wb")
        server_file_name = self.chat + self.sender + self.time + "0"
        k = code.code()
        k.key = key
        k.open_file_bytes(self.image_address)
        k.coding_with_open_key()
        k.save_code(path2("coded/" + server_file_name))
        file = open(path2("coded/" + server_file_name), mode="rb")
        send_file = {'file': (server_file_name, file)}
        payload = MultipartEncoder({'file': file})

        try:
            requests.post(data[5], files=send_file)
            is_sended = True
        except:
            is_sended = False
            error_connect()
        file.close()
        os.remove(path2("coded/" + server_file_name))
        if is_sended:
            requests.get(data[3], json={"chat": self.chat, "body": ["Image", self.time, data[0], self.name, [server_file_name]]})
    def open_image(self, tag):
        self.image_address = download_file_address("Images/" + self.name)
        if not self.had_downloaded:
            if not (self.image_address in imges):
                try:
                    server_file_name = self.chat + self.sender + self.time + "0"

                    resp = requests.get(data[6], json={"filename": server_file_name})
                    file = open(self.image_address, mode="wb")
                    file.write(resp.content)
                    file.close()

                    try:
                        width, height, channels, data_image = dpg.load_image(
                            download_file_address("Images/" + self.name))
                        with dpg.texture_registry(show=False):
                            k = height / width
                            dpg.add_static_texture(width=width, height=height, default_value=data_image)
                            self.tag = dpg.last_item()
                        dpg.add_image(texture_tag=self.tag, parent=tag, width=300, height=300 * k)
                        self.had_downloaded = True
                        imges.append(self.image_address)
                    except:
                        pass

                except ConnectionError:
                    error_connect()










class Text(Messages):

    def __init__(self, time, sender, chat, body, num_message, message_files_names):
        super(Text, self).__init__(time, sender, chat, num)
        self.body = body
        self.num = num_message
        self.time = time
        self.sender = sender
        self.chat = chat
        self.files_names = message_files_names
        if self.files_names == [""]:
            self.files_names = []
    def download_files(self):
        if self.files_names == [""]:
            self.files_names = []
            return
        num = 0
        with dpg.window(label="Загрузка файлов", height=200, width=400, no_close=True):
            tag = dpg.last_item()
            num_files = len(self.files_names)
            dpg.add_text("Загружено 0 из "+ str(num_files) + " файлов.", color=(155, 25, 255))
            with dpg.child_window():
                for name in self.files_names:
                    dpg.add_text(name, color=(25, 255, 25), wrap=300, bullet=True)
            for file_name in self.files_names:
                try:
                    server_file_name = self.chat + self.sender + self.time + str(num)
                    c = code.code()
                    c.key = key
                    c.bytes = bytes(server_file_name, "utf-8")
                    c.coding_with_open_key()
                    f_n = ""
                    for byte in c.koded:
                        f_n += str(int(byte))
                        f_n += " "
                    resp = requests.get(data[15] + "download_file_with_coding", json={"filename": f_n})
                    file = open(path2("coded/" + server_file_name), mode="wb")
                    file.write(resp.content)
                    file.close()
                    c.open_file_code(path2("coded/" + server_file_name))
                    c.decoding_with_open_key()
                    c.save_bytes(download_file_address(file_name))
                    os.remove(path2("coded/" + server_file_name))

                    num += 1
                    dpg.configure_item(tag + 1,
                                       default_value="Загружено " + str(num) + " из " + str(num_files) + " файлов.")
                    if data[12]=="True":
                        try:
                            if os.name == "posix":
                                try:
                                    subprocess.Popen(['open', download_file_address(file_name)])
                                except:
                                    subprocess.Popen(['see', download_file_address(file_name)])
                            elif os.name == "nt":
                                subprocess.Popen(['start', download_file_address(file_name)], shell=True)
                        except:sound_error()

                except :
                    with dpg.window(label="Ошибка", pos=(500, 300), width=300, height=200, modal=True,
                                    no_title_bar=True, no_move=True, no_resize=True):
                        dpg.add_text("Ошибка", color=(255, 25, 25), pos = (10, 10))
                        tag = dpg.last_item()
                    time.sleep(1)
                    dpg.delete_item(tag)
                    #break



        time.sleep(0.5)
        if dpg.is_item_ok(tag):
            dpg.delete_item(tag)
    def update_value(self, new_value):
        requests.get(data[4], json={"chat":self.chat, "num":self.num, "body":["Text", self.time, self.sender, new_value, self.files_names]})
    def delete(self):
        requests.get(data[7], json={"chat":self.chat, "time":self.time, "sender":self.sender, "num":self.num, "files":self.files_names, "type":"Text"})

    def send(self, files, tag2):
        try:
            with dpg.window(label="Отправка файлов", height=200, width=400, no_close=True):
                tag = dpg.last_item()
                tags = []
                n = [0]
                with dpg.child_window():
                    for file in files_names:
                        dpg.add_text(file, color=(255, 255, 255), wrap=300, bullet=True)
                        tags.append(dpg.last_item())

                num = 0
                is_sended = True


                for file in files:
                    def send(num, file):
                        server_file_name = self.chat + data[0] + self.time + str(num)
                        c = code.code()
                        c.key = key
                        c.open_file_bytes(file)
                        c.coding_with_open_key()
                        c.save_code(path2("coded/" + server_file_name))
                        c.bytes = bytes(server_file_name, "utf-8")
                        c.coding_with_open_key()
                        s_f_n_c = ""
                        for byte in c.koded:
                            s_f_n_c += str(int(byte))
                            s_f_n_c+=" "

                        dpg.configure_item(tags[num], color=(25, 25, 255))
                        file = open(path2("coded/" + server_file_name), mode="rb")
                        send_file = {'file': (s_f_n_c, file)}
                        payload = MultipartEncoder({'file': file})
                        try:
                            r = requests.post(data[15] + "send_file_with_coding", files=send_file)
                            if r.status_code != 200:
                                dpg.configure_item(tags[num], color=(255, 25, 25))
                            else:
                                dpg.configure_item(tags[num], color=(25, 255, 25))
                        except :

                            is_sended = False
                            dpg.configure_item(tags[num], color=(255, 25, 25))
                        file.close()
                        os.remove(path2("coded/" + server_file_name))
                        n[0] += 1
                    t = Thread(target=send, args=(num, file))
                    t.start()

                    num += 1

                while n[0] != num:
                    time.sleep(0.2)




                try:
                    if is_coding:
                        c = code.code()
                        c.key = key
                        body = {"chat": self.chat, "body": ["Text", self.time, self.sender, self.body, self.files_names]}
                        jsn = json.dumps(body)
                        c.bytes = bytes(jsn, "utf-8")
                        c.coding_with_open_key()
                        requests.get(data[15] + "send_with_coding", json=json.dumps(c.koded))
                    else:
                        requests.get(data[3], json={"chat": self.chat, "body": ["Text", self.time, self.sender, self.body, files_names]})
                except:
                    is_sended = False
                if is_sended:
                    files.clear()
                    files_names.clear()
                    time.sleep(0.5)
                    dpg.delete_item(tag)
                    dpg.configure_item(tag2, default_value="")
                else:
                    dpg.delete_item(tag)
                    error_connect()
        except :
            dpg.delete_item(tag)
            error_connect()




t8 = Thread(target = sound)# Уведомляем о том, что приложение запустилось
t8.start()







#
#
#
#Отрисовка
#
#
#

# Загрузка шрифтов
dpg.create_context()
with dpg.font_registry():
    with dpg.font(path2('notomono-regular.ttf'), 50, default_font=True, id="Default50"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('notomono-regular.ttf'), 25, default_font=True, id="Default25"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('ofont.ru_Times New Roman.ttf'), 25, default_font=True, id="Times25"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('ofont.ru_Times New Roman.ttf'), 50, default_font=True, id="Times50"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('notomono-regular.ttf'), 16, default_font=True, id="Default16"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('ofont.ru_Times New Roman.ttf'), 16, default_font=True, id="Times16"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('ofont.ru_Times New Roman.ttf'), 35, default_font=True, id="Times35"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font(path2('notomono-regular.ttf'), 35, default_font=True, id="Default35"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font(data[11])






# загрузка изображений
width, height, channels, data_image = dpg.load_image(path2("settings.jpeg"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="texture_tag")

width, height, channels1, data_image = dpg.load_image(path2("fon.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="texture_tag2")


width, height, channels2, data_image = dpg.load_image(path2("send_message.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="send")


width, height, channels3, data_image = dpg.load_image(path2("vlozh.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="vlozh")


width, height, channels4, data_image = dpg.load_image(path2("play.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="play")



width, height, channels5, data_image = dpg.load_image(path2("sounds_off.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="sounds_off")

width, height, channels6, data_image = dpg.load_image(path2("sounds_on.gif"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="sounds_on")


width, height, channels7, data_image = dpg.load_image(path2("Image.png"))
with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data_image, tag="Image")



listbox_value = ""

files_names = []
messages = {}
for address in address_book2:
    messages[address.addres] = []


def open_message(num, chat):
    message_open = messages[chat][num]
    window_tag = 0

    if type(message_open) == Text:
        def download_files():
            t = Thread(target=message_open.download_files)
            t.start()

        def update_message():
            value = dpg.get_value(window_tag + 2)

            message_open.update_value(value)

        def delete():
            message_open.delete()
            dpg.delete_item(window_tag)

        with dpg.window(label="Сообщение"):
            window_tag = dpg.last_item()
            # if
            if message_open.files_names != []:
                dpg.add_text("Файлы: " + str(message_open.files_names)[1:-1], wrap=500)
                dpg.add_button(label="Загрузить файлы", callback=download_files)
            else:
                dpg.add_text("Файлов нет")
            dpg.add_input_text(default_value=message_open.body, multiline=True, height=150)
            dpg.add_button(label="Изменить текст сообщения", callback=update_message)
            dpg.add_button(label="Удалить сообщение", callback=delete)


    elif type(message_open) == Sounds:
        def delete():
            message_open.delete()
            dpg.delete_item(window_tag)

        with dpg.window(label="Сообщение"):
            window_tag = dpg.last_item()
            dpg.add_text("Кто услышал:")
            for i in message_open.hears:
                dpg.add_text(i, color=(25, 255, 50))
            dpg.add_text("Кто увидел: ")
            for i in message_open.visions:
                dpg.add_text(i, color=(25, 25, 255))

            dpg.add_button(label="Удалить сообщение", callback=delete)




def update_item(item, chat_address, files_listbox_tag):#обновление списка сообщений на экране

    while is_run:
        messages[chat_address] = []

        try:
            dpg.is_item_shown(item - 1)
        except:
            break
        dpg.configure_item(files_listbox_tag, items = files_names)
        try:
            img = ["mvAppItemType::mvImage"]
            messages1 = []
            messages_text = []
            chat = chats_data[chat_address]
            num = 0
            x = 400
            y = 600
            ch = dpg.get_item_children(item)
            images_tags_x_y = {}
            for tag in dpg.get_item_children(item)[1]:
                if dpg.get_item_type(tag) in img:
                    try:
                        dpg.configure_item(tag, pos=images_tags_x_y[tag])
                    except:
                        pass
                else:
                    dpg.delete_item(tag)


            #pg.delete_item(item, children_only=True)
            messeges_nums_and_values = {}
            for message in chat:

                if type(message) == Text:
                    # messages[chataddress] = []
                    # messages[chataddress].append(Text(message[1], message[2], chataddress, message[3], num, message[4]))

                    out_text = str(message.time[:-7] + " " + message.sender + " " + message.body)
                    with dpg.group(horizontal=True, parent=item):
                        dpg.add_text(out_text, wrap=700, color=(255, 255, 255))
                        messeges_nums_and_values[out_text] = num
                        dpg.add_button(label="Открыть",
                                       callback=lambda s: open_message(messeges_nums_and_values[dpg.get_value(s - 1)],
                                                                       chat_address))
                elif type(message) == Sounds:
                    with dpg.group(horizontal=True):
                        out_text = str(message.time[:-7] + " " + message.sender)
                        dpg.add_text(out_text, wrap=500, color=(255, 255, 255))
                        dpg.add_image(texture_tag="sounds_on")
                        messeges_nums_and_values[out_text] = num
                        dpg.add_button(label="Открыть",
                                       callback=lambda s: open_message(messeges_nums_and_values[dpg.get_value(s - 2)],chat_address))
                        t10 = Thread(target=message.sound())
                        t10.start()
                elif type(message) == Images:

                    # image = Images(time = message[1], sender=message[2], chat = chataddress, num = 0, image_address= "", name = message[3])
                    # image.open_image(child_tag)
                    message.open_image(item)
                    dpg.add_text("Image")
                    images_tags_x_y[dpg.last_item() - 1] = dpg.get_item_pos(dpg.last_item())
                    images_tags_x_y[dpg.last_item() - 1][1] += 50
                elif message[0] == "Sound":
                    Sound = Sounds(message[1], message[2], chat_address, hears = message[3], num = num, visions=message[4])
                    messages1.append(Sound)
                    messages[chat_address].append(Sound)
                    with dpg.group(horizontal=True, parent=item):
                        out_text = str(message[1][:-7] + " " + message[2])
                        dpg.add_text(out_text, wrap=500, color=(255, 255, 255))
                        dpg.add_image(texture_tag="sounds_on")
                        messeges_nums_and_values[out_text] = num
                        dpg.add_button(label="Открыть", callback=lambda s: open_message(messeges_nums_and_values[dpg.get_value(s - 2)], chat_address))
                        t10 = Thread(target=Sound.sound())
                        t10.start()

                elif message[0] == "Image":
                    image = Images(message[1], message[2], chat_address, 0, message[3], "")
                    image.open_image(item)
                    img.append(image.image_address)
                    imges.append(image.image_address)
                    dpg.add_text("Image", parent=item)
                    images_tags_x_y[dpg.last_item() - 1] = dpg.get_item_pos(dpg.last_item())
                    images_tags_x_y[dpg.last_item() - 1][1] += 50
                    messages1.append(image)
                    messages[chat_address].append(image)
                num += 1

            #for i in messages1:
            #    messages[chat_address].append(i)
        except ConnectionError:
            pass

        time.sleep(0.5)

def show_name_editor():
    tag = [0]
    def save_new_name():
        name = dpg.get_value(tag[0])
        dpg.set_value("Основная заставка", "Привет, " + name + "!")
        data[0] = name
        file_data = open(os.path.join(pth, "files", "data.txt"), mode="w")
        for i in data:
            print(i, file=file_data)
        file_data.close()
    with dpg.window(label="Изменить имя", width=500):
        dpg.add_text("Введите новое имя:")
        dpg.add_input_text(hint="Иванов Иван Петрович")
        tag[0] = dpg.last_item()
        dpg.add_button(label="Изменить имя", callback=save_new_name)








def error_connect():
    with dpg.window(label="Ошибка подключения", pos=(500, 300), width=320, height=100, modal=True, no_title_bar=True, no_move=True, no_resize=True):
        def delete():
            dpg.delete_item(dpg.last_item()-2)
        dpg.add_text("Ошибка подключения", color=(255, 0, 0, 255))
        dpg.add_button(label="Отмена", callback=delete, pos=(200, 50))
        sound_error()


def render_messages():#функция открывает чаты или меню для добавления нового контакта
    file_dialog_tag = [0]
    try:
        files_list = {}
        files = []
        n = 0

        def clear_chat():
            with dpg.window(label="Очистка истории", pos=(500, 300), width=300, height=200, modal=True, no_title_bar=True, no_move=True, no_resize=True):
                dpg.add_text("Вся история чата будет удалена! Введите ниже цифры: 12345678",
                             color=(255, 20, 20, 255), wrap=250)
                dpg.add_input_text(label=" ", password=True)
                tag = dpg.last_item()

                def escape():
                    dpg.delete_item(tag - 2)

                def clear_chat1():
                    if dpg.get_value(tag) == "12345678":
                        requests.get(data[9], json={"chat": chataddress})
                        dpg.delete_item(tag - 2)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Очистить", callback=clear_chat1)
                    dpg.add_button(label="Отмена", callback=escape)
        def delete_file():
            value = dpg.get_value(files_listbox_tag)
            num_file = files_list[value]
            files.pop(num_file)
            files_names.pop(num_file)

        def open_file_list():
            with dpg.file_dialog(callback=add_file, height=500):
                file_dialog_tag[0] = dpg.last_item()
                dpg.add_file_extension(".*", color=(255, 255, 255, 255))
                dpg.add_file_extension(".jpeg", color=(25, 255, 25, 255))
                dpg.add_file_extension(".jpg", color=(25, 255, 25, 255))
                dpg.add_file_extension(".exec", color=(255, 25, 25, 255))
                dpg.add_file_extension(".exe", color=(255, 25, 25, 255))
                dpg.add_file_extension(".png", color=(25, 255, 25, 255))
                dpg.add_file_extension(".JPG", color=(25, 255, 25, 255))
                dpg.add_file_extension(".txt", color=(105, 105, 255, 255))
                dpg.add_file_extension(".rar", color=(255, 25, 255, 255))
                dpg.add_file_extension(".RAR", color=(255, 25, 255, 255))
                dpg.add_file_extension(".zip", color=(255, 25, 255, 255))
                dpg.add_file_extension(".ZIP", color=(255, 25, 255, 255))
                dpg.add_file_extension(".bmp", color=(25, 255, 25, 255))
                dpg.add_file_extension(".doc", color=(255, 25, 255, 255))
                dpg.add_file_extension(".docm", color=(255, 25, 255, 255))
                dpg.add_file_extension(".docx", color=(255, 25, 255, 255))
                dpg.add_file_extension(".dot", color=(255, 25, 255, 255))
                dpg.add_file_extension(".dotx", color=(255, 25, 255, 255))
                dpg.add_file_extension(".gif", color=(25, 255, 25, 255))
                dpg.add_file_extension(".jar", color=(255, 25, 255, 255))
                dpg.add_file_extension(".mov", color=(255, 25, 255, 255))
                dpg.add_file_extension(".mp4", color=(255, 25, 255, 255))
                dpg.add_file_extension(".mpeg", color=(25, 255, 25, 255))
                dpg.add_file_extension(".pdf", color=(255, 25, 255, 255))
                dpg.add_file_extension(".ppt", color=(255, 25, 255, 255))
                dpg.add_file_extension(".pptm", color=(255, 25, 255, 255))
                dpg.add_file_extension(".pptx", color=(255, 25, 255, 255))
                dpg.add_file_extension(".psd", color=(255, 25, 255, 255))
                dpg.add_file_extension(".tif", color=(25, 255, 25, 255))
                dpg.add_file_extension(".tiff", color=(25, 255, 25, 255))
                dpg.add_file_extension(".wav", color=(255, 25, 255, 255))
                dpg.add_file_extension(".ttf", color=(255, 25, 255, 255))
                dpg.add_file_extension(".dll", color=(255, 25, 25, 255))
                dpg.add_file_extension(".py", color=(255, 25, 255, 255))
                dpg.add_file_extension(".c", color=(255, 25, 255, 255))
                dpg.add_file_extension(".cpp", color=(255, 25, 255, 255))
                dpg.add_file_extension(".java", color=(255, 25, 255, 255))
                dpg.add_file_extension(".class", color=(255, 25, 255, 255))
                dpg.add_file_extension(".mp3", color=(25, 255, 25, 255))
                dpg.add_file_extension(".avi", color=(255, 25, 255, 255))



        def add_file():
            try:
                a = dpg.get_file_dialog_info(file_dialog_tag[0])
                n = 1
                if a != {'file_path_name': '/Users/artembatanin/PycharmProjects/messenger/.*', 'file_name': '.*',
                         'current_path': '/Users/artembatanin/PycharmProjects/messenger', 'current_filter': '.*',
                         'min_size': [100.0, 100.0], 'max_size': [30000.0, 30000.0], 'selections': {}}:
                    for file_address in str(a["selections"].values()).split(sep="'"):
                        if n == -1:

                            files.append(file_address)
                            file_name = os.path.basename(file_address)
                            files_names.append(file_name)
                            files_list[file_name] = len(files_names) - 1
                            dpg.set_value(dpg.last_item() - 1, "")
                        n *= -1
            except :
                def delete_wind():
                    dpg.delete_item(dpg.last_item()-2)
                with dpg.window(label="Ошибка", modal=True, no_move=True, no_title_bar=True, pos=(500, 300)):
                    dpg.add_text("Неверный путь до файла", color=(255, 25, 25))
                    dpg.add_button(label="Отмена", callback=delete_wind)
        def send_image():
            a = dpg.get_file_dialog_info(file_dialog_tag[0])
            n = 1
            if a != {'file_path_name': '/Users/artembatanin/PycharmProjects/messenger/.*', 'file_name': '.*',
                     'current_path': '/Users/artembatanin/PycharmProjects/messenger', 'current_filter': '.*',
                     'min_size': [100.0, 100.0], 'max_size': [30000.0, 30000.0], 'selections': {}}:
                for file_address in str(a["selections"].values()).split(sep="'"):
                    if n == -1:
                        file_name = os.path.basename(file_address)
                        image = Images(str(datetime.datetime.now()), data[0], chataddress, 0, name=file_name, image_address=file_address)
                        image.send()
                    n *= -1


        def open_image():
            with dpg.file_dialog(callback=send_image, height=500):
                file_dialog_tag[0] = dpg.last_item()
                dpg.add_file_extension(".jpeg", color=(25, 255, 25, 255))
                dpg.add_file_extension(".jpg", color=(25, 255, 25, 255))
                dpg.add_file_extension(".JPG", color=(25, 255, 25, 255))
                dpg.add_file_extension(".png", color=(25, 255, 25, 255))
                dpg.add_file_extension(".PNG", color=(25, 255, 25, 255))
                dpg.add_file_extension(".gif", color=(25, 255, 25, 255))
                dpg.add_file_extension(".jpg", color=(25, 255, 25, 255))


        def send_text_message():
            text = dpg.get_value(tag)

            if text != "" and text != " " and text != "  " and text != "    ":
                message = Text(str(datetime.datetime.now()), data[0], chataddress, text, 0, files_names)
                t3 = Thread(target=message.send, args=(files, tag))
                t3.start()
        def send_sound_message():
            Sound = Sounds(0, [], chataddress, [], len(messages), visions=[])
            Sound.send()

        def delete():
            address_book2.remove(obj)
            names = []
            for i in address_book2:
                names.append(i.name)
            names.append("+")
            dpg.configure_item("Адресная книга", items=names)
            write_to_file()
            dpg.delete_item(window_tag)

        listbox_value = dpg.get_value("Адресная книга")


        if "+" == listbox_value:
            show_menu_add_new_contact()
        for num in range(0, len(address_book2)):
            i = address_book2[num]
            if i.name == listbox_value:
                obj = i
                with dpg.window(label="Окно чата"):#pos=(0, 0), no_title_bar=True, no_resize= True, width=1500, height=1000, no_move=True):
                    window_tag = dpg.last_item()
                    dpg.add_text(i.name)
                    dpg.add_text(i.addres)
                    dpg.add_button(width=50, height=50, pos=(870, 640), callback=send_sound_message)
                    dpg.add_image("sounds_on", pos=(870, 640), width=50, height=50)
                    dpg.add_button(label="Удалить", callback=delete)
                    dpg.add_input_text(pos=(150, 530), width=700, multiline=True, height=150)
                    tag = dpg.last_item()
                    dpg.add_button(width=50, height=50, pos=(870, 540), callback=send_text_message)
                    dpg.add_button(pos=(930, 540), width=50, height=50, callback=open_file_list)
                    dpg.add_image("send", pos=(870, 540), width=50, height=50)
                    dpg.add_image("vlozh", pos=(930, 540), width=50, height=50)
                    dpg.add_button(pos =(930, 640), width=50, height= 50, callback=open_image)
                    dpg.add_image("Image", pos=(930, 640), width=50, height= 50)
                    dpg.add_listbox(files_names, num_items=3, pos=(50, 700), width=900, callback=delete_file)
                    files_listbox_tag = dpg.last_item()
                    dpg.bind_item_font(files_listbox_tag, "Default16")
                    dpg.add_button(label="Очистить", callback=clear_chat, pos=(830, 50))

                    with dpg.tooltip(tag - 2):
                        dpg.add_text("Отправить уведомление", color=(20, 255, 0, 255))
                    with dpg.tooltip(tag - 1):
                        dpg.add_text("Удалить контакт", color=(255, 10, 10, 255))
                    with dpg.tooltip(tag):
                        dpg.add_text("Введите текст сообщения", color=(20, 255, 0, 255))
                    with dpg.tooltip(tag + 1):
                        dpg.add_text("Отправить сообщение", color=(20, 255, 0, 255))
                    with dpg.tooltip(tag + 2):
                        dpg.add_text("Добавить вложение", color=(20, 255, 0, 255))
                    with dpg.tooltip(tag + 7):
                        dpg.add_text("Открепить файл", color=(255, 0, 255))
                    with dpg.tooltip(tag + 8):
                        dpg.add_text("Вся история чата будет удалена! Нажимайте только если вы знаете что делаете.",
                                     color=(255, 20, 20, 255), wrap=250)
                    with dpg.tooltip(tag+6):
                        dpg.add_text("Добавить картинку", color = (25, 255, 25, 255))

                    try:
                        chataddress = i.addres
                        messages.clear()
                        chat = chats_data[chataddress]
                        num = 0
                        messeges_nums_and_values = {}
                        x = 400
                        y = 600
                        with dpg.child_window(pos=(150, 100), width=850, height= 400):
                            child_tag = dpg.last_item()
                            for message in chat:

                                if type(message) == Text:
                                   #messages[chataddress] = []
                                    #messages[chataddress].append(Text(message[1], message[2], chataddress, message[3], num, message[4]))

                                    out_text = str(message.time[:-7] + " " + message.sender + " " + message.body)
                                    with dpg.group(horizontal=True):
                                        dpg.add_text(out_text, wrap = 700, color = (255, 255, 255))
                                        messeges_nums_and_values[out_text] = num + 1
                                        dpg.add_button(label="Открыть", callback= lambda s: open_message(messeges_nums_and_values[dpg.get_value(s - 1)], chataddress))
                                elif type(message) == Sounds:
                                    with dpg.group(horizontal=True):
                                        out_text = str(message.time[:-7] + " " + message.sender)
                                        dpg.add_text(out_text, wrap=500, color = (255, 255, 255))
                                        dpg.add_image(texture_tag="sounds_on")
                                        messeges_nums_and_values[out_text] = num + 1
                                        dpg.add_button(label="Открыть", callback=lambda s: open_message(messeges_nums_and_values[dpg.get_value(s - 2)], chataddress))
                                elif type(message) == Images:

                                    #image = Images(time = message[1], sender=message[2], chat = chataddress, num = 0, image_address= "", name = message[3])
                                    #image.open_image(child_tag)
                                    message.open_image(child_tag)
                                    dpg.add_text("Image")

                                num += 1
                            imges.clear()
                            t2 = Thread(target=update_item, args=(child_tag, i.addres, files_listbox_tag))
                            t2.start()




                    except requests.exceptions.ConnectionError:
                        error_connect()

    except ZeroDivisionError:
        dpg.delete_item(dpg.last_item())
        error_connect()




def update_is_connection():
    while is_run:
        try:
            if is_connect["now"] == True:
                dpg.configure_item("is_connected", fill = (20, 25, 250, 255))
                time.sleep(0.05)
                dpg.configure_item("is_connected", fill=(20, 255, 20, 255))
            else:
                dpg.configure_item("is_connected", fill=(255, 0, 0, 255))

        except:
            pass
        time.sleep(1)





def show_editor():
    dpg.show_style_editor()

def show_menu_add_new_contact():#открывает меню для добавления нового контакта
    tag = [0, 0]
    def add_contact_to_address_boook():  # функция добавляет контакт в массив и загружает массив в файл
        name = dpg.get_value(tag[0])
        address = dpg.get_value(tag[1])
        address_book2.append(addresses(name, address))
        names = []
        for i in address_book2:
            names.append(i.name)
        names.append("+")
        dpg.configure_item("Адресная книга", items=names)
        write_to_file()
        is_connect["time"][address] = []
        t = Thread(target=update_chat, args=(addresses(name, address),))
        t.start()
    with dpg.window(label="Добавить контакт", width=350):
        dpg.add_input_text(label="Имя", hint="Название контакта")
        dpg.add_input_text(label="Адрес", hint="Адрес контакта")
        dpg.add_button(label="Добавить контакт", callback=add_contact_to_address_boook)
        tag[0] = dpg.last_item() - 2
        tag[1] = dpg.last_item() - 1






def show_settings():
    a = ["Елизавете Александровне Батаниной", "Зинаиде Васильевне Зыковой", "Разработчикам dearpygui","Разработчикам Flask", "Разработчикам dearimgui"]
    with dpg.window(label="Настройки", no_move=True, no_collapse=True, no_resize=True, height=800, width=700):
        tag = dpg.last_item()
        def update_plot():
            while is_run:
                try:
                    try:
                        req = requests.get(data[10], json="1")
                        dpg.configure_item(plot - 2, default_value=req.json()[1], color=(25, 25, 255))
                    except:
                        pass
                    pass
                except:
                    pass
                mx = []
                for i in series_tags.keys():
                    mx += is_connect["time"][i]
                    dpg.configure_item(series_tags[i], x=is_connect["num"][i], y=is_connect["time"][i])

                dpg.set_axis_limits(yaxis, 0, max(mx))
                time.sleep(1)
        def bind_font():
            value = dpg.get_value(tag + 3)
            data[11] = str(value)
            dat = open(path2("data.txt"), mode="w")
            for i in data:
                dat.write(i+"\n")
            dat.close()
            dpg.configure_item(tag+2, default_value=data[11])
        def update_open_massages():
            value = dpg.get_value(tag + 8)
            data[12] = str(value)
            dat = open(path2("data.txt"), mode="w")
            for i in data:
                dat.write(i + "\n")
            dat.close()
        def update_sound():
            value = dpg.get_value(tag + 11)
            data[13] = str(value)
            dat = open(path2("data.txt"), mode="w")
            for i in data:
                dat.write(i + "\n")
            dat.close()

        dpg.add_text("Настройка шрифта", bullet=True)
        items = ["Default16", "Default25", "Default35", "Default50", "Times16", "Times25", "Times35", "Times50"]
        with dpg.group(horizontal = True):
            dpg.add_listbox(items=items, callback=bind_font, default_value=data[11], num_items=4)
            dpg.add_button(label="Дополнительно", callback=lambda : dpg.show_style_editor())
        dpg.add_text("*Перезапустите приложение что бы изменения вступили в силу", wrap=600)
        with dpg.group(horizontal=True):
            dpg.add_text("Открывать файлы автоматически?")
            if data[12] == "True":
                def_value = True
            else:
                def_value = False

            dpg.add_checkbox(default_value=def_value, callback=update_open_massages)
        with dpg.group(horizontal=True):
            dpg.add_text("Звук")
            if data[13] == "True":
                def_value = True
            else:
                def_value = False
            dpg.add_checkbox(default_value=def_value, callback=update_sound)




        with dpg.group(horizontal=True):
            dpg.add_text("Место сохранения")
            tag_input_text = dpg.last_item() + 2
            def save_path_to_save():

                path = dpg.get_value(tag_input_text)
                data[14] = path
                dat = open(path2("data.txt"), mode="w")
                for i in data:
                    dat.write(i + "\n")
                dat.close()
            with dpg.group():
                dpg.add_input_text(default_value=data[14])
                dpg.add_button(label="Сохранить", callback=save_path_to_save)



        with dpg.group(horizontal=True):
            try:
                req = requests.get(data[10], json="1")
                dpg.add_text(req.json()["1"], bullet=True, color=(25, 25, 205), wrap=600)
            except:
                dpg.add_text("Нет подключения к серверу", color=(255, 25, 25))
        dpg.add_text("Ping(sec):", bullet=True)
        series_tags = {}
        dpg.add_text("Версия 1.06 Beta", color=(25, 255, 50))

        with dpg.plot(width=650):
            plot = dpg.last_item()
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis)
            xaxis = dpg.last_item()
            dpg.set_axis_limits(xaxis, 0, 40)
            dpg.add_plot_axis(dpg.mvYAxis)
            yaxis = dpg.last_item()
            dpg.set_axis_limits_auto(yaxis)
            for i in address_book2:
                dpg.add_line_series(is_connect["num"][i.addres], is_connect["time"][i.addres], parent=yaxis, label=i.name)
                series_tags[i.addres] = (dpg.last_item())
        dpg.bind_item_theme(plot, plot_theme)
        t = Thread(target=update_plot)
        t.start()

        dpg.add_text("Огромное спаибо за помошь в разработке:")
        col1 = 0
        col2 = 255
        dcol = 255/len(a)
        with dpg.child_window(label="Огромное спасибо", height = 400, width = 600):
            for i in a:
                dpg.add_text(i, color=(col1, 255, col2), bullet=True, wrap = 580)
                col1 += dcol
                col2 -=dcol


def open_files_media():
    class open_file:
        file_dialog = 0

        def __init__(self, file_addres, wind_tag):
            self.tag = 0
            self.name = ""
            self.n = 0
            self.height = 0
            self.width = 0
            self.file_addres = file_addres
            self.wind_tag = wind_tag
        def open(self):
            types1 = ["txt", "cpp", "py", "c", "java", "H", "h"]
            types2 = ["wav"]
            types3 = ["jpg", "JPG", "jpeg", "Jpeg", "Jpg", "png", "PNG", "webp", "tiff", "Tiff", "TIFF"]
            if self.file_addres.split(".")[1] in types1:
                try:
                    dpg.delete_item(self.wind_tag + 1, children_only=True)
                except:
                    pass
                file = open(self.file_addres, mode = "r")
                output_text = file.read()
                file.close()
                dpg.add_input_text(default_value=output_text, parent=self.wind_tag + 1, pos=(10, 140), width=900, multiline=True, height=500)

                self.tag = dpg.last_item()
                address = self.file_addres
                tag = self.tag
                def save():
                    file2 = open(address, mode = "w")
                    file2.write(dpg.get_value(tag))
                    file2.close()
                dpg.add_button(label = "Сохранить", callback=save, parent=self.wind_tag + 1)
                self.width = 900
                self.height = 500
            elif self.file_addres.split(".")[1] in types2:
                try:
                    dpg.delete_item(self.wind_tag + 1, children_only=True)
                except:
                    pass
                filename = self.file_addres
                wave_object = simple_audio.WaveObject.from_wave_file(filename)
                play_object = wave_object.play()
                play_object.wait_done()
                #self.tag = dpg.last_item()
            elif self.file_addres.split(".")[1] in types3:
                width, height, channels, data_image = dpg.load_image(self.file_addres)
                self.width = width
                self.height = height
                try:
                    dpg.delete_item(self.wind_tag + 1, children_only=True)
                except:
                    pass

                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width=width, height=height, default_value=data_image)
                    self.n = 500 / width
                    dpg.add_image(dpg.last_item(), width=self.width * self.n, height=self.height * self.n, pos=(0, 140),
                                  parent=self.wind_tag + 1)
                    self.tag = dpg.last_item()
            else:
                if os.name == "posix":
                    try:
                        subprocess.Popen(['open', self.file_addres])
                    except:
                        subprocess.Popen(['see', self.file_addres])
                elif os.name == "nt":
                    subprocess.Popen(['start', self.file_addres], shell=True)

        def close(self):
            dpg.delete_item(self.tag)
        def plus(self):
            self.n *= 1.1
            dpg.configure_item(self.tag, width = self.width * self.n, height = self.height * self.n)

        def minus(self):
            self.n /= 1.1
            dpg.configure_item(self.tag, width=self.width * self.n, height=self.height * self.n)
        def new_val(self, n):
            self.n = n
            dpg.configure_item(self.tag, width=self.width * self.n, height=self.height * self.n)
    def open_media():
        a = dpg.get_file_dialog_info(file_dialog)
        if a != {'file_path_name': '/Users/artembatanin/PycharmProjects/messenger/.*', 'file_name': '.*',
                 'current_path': '/Users/artembatanin/PycharmProjects/messenger', 'current_filter': '.*',
                 'min_size': [100.0, 100.0], 'max_size': [30000.0, 30000.0], 'selections': {}}:
            files_opend = []
            for file_address in str(a["selections"].values()).split(sep="'"):
                file_types = ["jpg", "JPG", "jpeg", "Jpeg", "Jpg", "png", "PNG", "webp", "tiff", "Tiff", "TIFF", "txt", "wav", "mp3", "mp4", "MP3", "MP4", "pptx", "pdf", "doc", "xlsx", "webm", "html", "3GP", "py", "cpp", "c", "java", "class", "zip", "ZIP", "rar", "RAR", "torrent", "exe", "dmg", "H", "h", "avi", "dot", "dotx", "mov", "exec", "gif", "jar", "ppt", "pptx", "pptm", "psd", "dll"]
                if file_address.split(sep=".")[-1] in file_types:
                    files_opend.append(file_address)
            with dpg.window(label = "Файлы", pos=(0, 0)):
                wind_tag = dpg.last_item()
                with dpg.child_window(pos=(10, 150)):
                    #dpg.add_image("texture_tag", width=100, height=100, pos=(0, 140))
                    def callb():
                        im = open_file(dpg.get_value(wind_tag + 2), wind_tag)
                        im.open()

                        def plus():
                            im.plus()
                        def minus():
                            im.minus()
                        dpg.add_button(label="+", pos=(0, 100), callback=plus, parent = wind_tag + 1)
                        dpg.add_button(label="-", pos=(50, 100), callback=minus, parent=wind_tag + 1)
                        def new_value():
                            val = dpg.get_value(im.tag + 3)
                            if str(type(val)) == "<class 'NoneType'>":

                                pass
                            else:
                                im.new_val(val)
                        dpg.add_slider_float(parent = wind_tag + 1, callback= new_value, max_value= 2, min_value= 0.1, default_value= 0.1)


                dpg.add_listbox(items=files_opend, callback=callb, pos=(10, 50))






    with dpg.file_dialog(callback=open_media, height=500, default_path=download_file_address("")):
        file_dialog = dpg.last_item()
        dpg.add_file_extension(".*", color=(255, 255, 255, 255))
        dpg.add_file_extension(".jpeg", color=(25, 255, 25, 255))
        dpg.add_file_extension(".jpg", color=(25, 255, 25, 255))
        dpg.add_file_extension(".exec", color=(255, 25, 25, 255))
        dpg.add_file_extension(".exe", color=(255, 25, 25, 255))
        dpg.add_file_extension(".png", color=(25, 255, 25, 255))
        dpg.add_file_extension(".JPG", color=(25, 255, 25, 255))
        dpg.add_file_extension(".txt", color=(105, 105, 255, 255))
        dpg.add_file_extension(".rar", color=(255, 25, 255, 255))
        dpg.add_file_extension(".RAR", color=(255, 25, 255, 255))
        dpg.add_file_extension(".zip", color=(255, 25, 255, 255))
        dpg.add_file_extension(".ZIP", color=(255, 25, 255, 255))
        dpg.add_file_extension(".bmp", color=(25, 255, 25, 255))
        dpg.add_file_extension(".doc", color=(255, 25, 255, 255))
        dpg.add_file_extension(".docm", color=(255, 25, 255, 255))
        dpg.add_file_extension(".docx", color=(255, 25, 255, 255))
        dpg.add_file_extension(".dot", color=(255, 25, 255, 255))
        dpg.add_file_extension(".dotx", color=(255, 25, 255, 255))
        dpg.add_file_extension(".gif", color=(25, 255, 25, 255))
        dpg.add_file_extension(".jar", color=(255, 25, 255, 255))
        dpg.add_file_extension(".mov", color=(255, 25, 255, 255))
        dpg.add_file_extension(".mp4", color=(255, 25, 255, 255))
        dpg.add_file_extension(".mpeg", color=(25, 255, 25, 255))
        dpg.add_file_extension(".pdf", color=(255, 25, 255, 255))
        dpg.add_file_extension(".ppt", color=(255, 25, 255, 255))
        dpg.add_file_extension(".pptm", color=(255, 25, 255, 255))
        dpg.add_file_extension(".pptx", color=(255, 25, 255, 255))
        dpg.add_file_extension(".psd", color=(255, 25, 255, 255))
        dpg.add_file_extension(".tif", color=(25, 255, 25, 255))
        dpg.add_file_extension(".tiff", color=(25, 255, 25, 255))
        dpg.add_file_extension(".wav", color=(255, 25, 255, 255))
        dpg.add_file_extension(".ttf", color=(255, 25, 255, 255))
        dpg.add_file_extension(".dll", color=(255, 25, 25, 255))
        dpg.add_file_extension(".py", color=(255, 25, 255, 255))
        dpg.add_file_extension(".c", color=(255, 25, 255, 255))
        dpg.add_file_extension(".cpp", color=(255, 25, 255, 255))
        dpg.add_file_extension(".java", color=(255, 25, 255, 255))
        dpg.add_file_extension(".class", color=(255, 25, 255, 255))
        dpg.add_file_extension(".mp3", color=(25, 255, 25, 255))
        dpg.add_file_extension(".avi", color=(255, 25, 255, 255))






dpg.create_context()
dpg.create_viewport(title='Мессенджер', width=1500, height=900)
with dpg.window(width=1450, height=900, no_title_bar=True, pos=(0, 0), no_move=True, no_resize=True, tag="Window", no_collapse= True, no_bring_to_front_on_focus=True):

    dpg.add_image(texture_tag="texture_tag2", width = 1400, height=890, pos=(0, 0))
    names = []
    for i in address_book2:
        names.append(i.name)
    names.append("+")
    dpg.add_listbox(names, pos=((200, 150)), tag="Адресная книга", callback=render_messages, num_items=15)
    dpg.add_loading_indicator(color=(25, 25, 255, 255), secondary_color=(25, 105, 255), tag="Loading", pos= (175, 35))
    dpg.add_text("Привет, "+data[0]+"!", pos=(300, 50), color=(0, 0, 0, 255), tag="Основная заставка", wrap=900)
    dpg.bind_item_font("Основная заставка", "Default50")
    dpg.add_button(label="+",width=100, height=100, pos=(0, 140), callback=show_settings)
    dpg.add_image("texture_tag", width=100, height=100, pos=(0,140), tag="Настройки")
    dpg.add_button(tag="кнопка изменить имя", pos = (1000, 50), width=50, height = 50, show=True, callback=show_name_editor)
    dpg.add_text("*", pos=(1012, 55), color=(0, 0, 0), tag="Изменить имя")
    dpg.bind_item_font("Изменить имя", 'Times50')
    dpg.draw_circle((50, 50), 25, color=(125, 125, 125, 255), fill=(125, 125, 125, 255))
    dpg.draw_circle((50, 50), 20, color=(125, 125, 125, 255), fill=(255, 0, 0, 255), tag="is_connected")
    dpg.add_button(pos=(5, 290), tag="Кнопка открыть проигрыватель", width=100, height=100, callback= open_files_media)
    dpg.add_image("play", pos=(5, 290), tag="Проигрыватель", width=100, height=100)
    t = Thread(target=update_is_connection)
    t.start()
    with dpg.tooltip("Настройки"):
        dpg.add_text("Открыть настройки", color=(255, 0, 255, 255))
    with dpg.tooltip("Адресная книга"):
        dpg.add_text("Открыть или добавить контакт", color=(20, 255, 0, 255))
    with dpg.tooltip("кнопка изменить имя"):
        dpg.add_text("Изменить имя", color=(255, 0, 255))
    with dpg.tooltip("Кнопка открыть проигрыватель"):
        dpg.add_text("Открыть загруженые файлы", color = (255, 0, 255))



with dpg.theme() as item_theme:

    with dpg.theme_component(dpg.mvListbox):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)


    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

with dpg.theme() as main_theme:

    with dpg.theme_component(dpg.mvListbox):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50, 255), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvWindowAppItem):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255, 235), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255), category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvPlotStyleVar_MinorAlpha, 2, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (25, 25, 25, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (15, 75, 15, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, category=dpg.mvThemeCat_Core)

with dpg.theme() as plot_theme:

    with dpg.theme_component(dpg.mvAll):

        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 55, 25, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255), category=dpg.mvThemeCat_Core)



dpg.bind_theme(main_theme)
dpg.bind_item_theme("Адресная книга", item_theme)
dpg.bind_item_theme("кнопка изменить имя", item_theme)
dpg.bind_item_theme("Кнопка открыть проигрыватель", item_theme)




dpg.create_viewport(title='Postmaster', width=1440, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()
is_run = False
sys.exit()