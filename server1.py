from flask import Flask, request, send_from_directory
import pickle
import os
from threading import Thread
import time
import datetime
import code
#import sys

black_ips = []
data_users_ip = {}
data_ips = []

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Server data")
path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Server data", "suite")
print(path)
time.sleep(2)
app = Flask(__name__)
try:
    with open(os.path.join(path,'data.dat'), 'rb') as f:
        messages = pickle.load(f)  # chatadress:[body1, body2, body3]
        print(messages)
except FileNotFoundError:
    messages = {}



try:
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ivent_data.close()

except:
    ivent_data1 = open(os.path.join(path,"ivent_data.txt"), "w")
    ivent_data1.close()


try:
    with open(os.path.join(path,'data_users_ip.dat'), 'rb') as f:
        data_users_ip = pickle.load(f)
        print(data_users_ip)
    f.close()
except:
    with open(os.path.join(path, 'data_users_ip.dat'), 'wb') as f:
        data_users_ip = {}
    f.close()



try:
    with open(os.path.join(path,'data_black_ips.dat'), 'r') as f:
        black_ips = f.read().split("\n")  # chatadress:[body1, body2, body3]
    f.close()
except:
    print("Black ips file is null")
    f.close()
    with open(os.path.join(path, 'data_black_ips.dat'), 'w') as f:
        pass
    f.close()


try:
    with open(os.path.join(path,'data_ips.dat'), 'r') as f:
        data_ips = f.read().split("\n")
    f.close()
except:
    with open(os.path.join(path, 'data_ips.dat'), 'w') as f:
        pass
    f.close()



files = {} # file.png addreess: file.png
#json={"chat": chataddress, "body": ("Text", time_now, data[0], text, files_names)} структура сообщения
is_run = True
def write_to_file():
        while is_run:
            time.sleep(1)
            with open(os.path.join(path,'data.dat'), 'wb') as f:
                pickle.dump(messages, f)
            f.close()
            with open(os.path.join(path, 'data_users_ip.dat'), 'wb') as f2:
                pickle.dump(data_users_ip, f2)
            f2.close()

            with open(os.path.join(path, 'data_ips.dat'), 'w') as f3:
                for i in data_ips:
                    f3.write(i + "\n")
            f3.close()

            try:
                with open(os.path.join(path, 'data_black_ips.dat'), 'r') as f:
                    black_ips.clear()
                    for i in f.read().split("\n"):
                        black_ips.append(i)
                f.close()
            except:
                print("Black ips file is null")
                f.close()
                with open(os.path.join(path, 'data_black_ips.dat'), 'w') as f:
                    pass
                f.close()

t = Thread(target=write_to_file)
t.start()

def delete_file(chat, sender, time, num):
    filename = chat + sender + time + str(num)
    print(filename)
    os.remove(os.path.join(path, filename.replace(':', '_')))





@app.route("/")
def HTTP():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    return send_from_directory(path2, "myfile.html")



@app.route("/get_ips")
def get_ips():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    rl = ""
    for i in data_users_ip.keys():
        rl += str(i) + " : " + str(data_users_ip[i]) + "\n"
    rl += "data ip: "
    for i in data_ips:
        rl += i + "\n"

    return rl


@app.route("/add_black_ip")
def add_black_ip():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1: 1}
    body = request.get_json()
    if body["Password"] == "333121333Aa":
        ivent_data = open(os.path.join(path, "ivent_data.txt"), "a")
        print("add_black_ip", " ", time, " ", ip, "", body["ip"], " ",  file=ivent_data)
        black_ips.append(body["ip"])
        return {1: "OK"}
    else:
        ivent_data = open(os.path.join(path, "ivent_data.txt"), "a")
        print("add_black_ip", " ", time, " ", ip, "", "Password is not valid", " ", file=ivent_data)
        return {1: "Error"}


@app.route("/delete_black_ip")
def delete_black_ip():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1: 1}
    body = request.get_json()
    if body["Password"] == "333121333Aa":
        ivent_data = open(os.path.join(path, "ivent_data.txt"), "a")
        print("delete_black_ip", " ", time, " ", ip, "", body["ip"], " ",  file=ivent_data)
        black_ips.remove(body["ip"])
        return {1: "OK"}
    else:
        ivent_data = open(os.path.join(path, "ivent_data.txt"), "a")
        print("delete_black_ip", " ", time, " ", ip, "", "Password is not valid", " ", file=ivent_data)
        return {1: "Error"}






@app.route("/ivent_data")
def ivent_data():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    data_ips.append(ip)
    return send_from_directory(path, "ivent_data.txt")
@app.route("/Windows")
def Windows():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "main_Windows.rar")
@app.route("/Mac")
def Mac():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "main_Mac.zip")
@app.route("/Linux")
def Linux():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "main_Linux.zip")


@app.route("/Picture1")
def Picture1():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "fon.png")

@app.route("/download_troyan")
def download_troyan():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "vidichka.mov")

@app.route("/Balbesy")
def Balbesy():
    ivent_data = open(os.path.join(path, "ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    time = str(datetime.datetime.now())
    print("Balbesy", " ", time, " ", ip, "", file=ivent_data)
    ivent_data.close()
    return send_from_directory(path2, "Balbesy.html")
@app.route("/Maximka_super")
def Maximka_super():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "IMG_9971.3GP")
@app.route("/Maximka_super2")
def Maximka_super2():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "IMG_9977.3GP")

@app.route("/Picture_maxim")
def Picture_maxim():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "DSC04088.JPG")

@app.route("/Picture_balbesy")
def Picture_balbesy():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "IMG-20220422-WA0001.jpg")
@app.route("/Picture_liza")
def Picture_liza():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "DSC00010.JPG")
@app.route("/Picture_babushka")
def Picture_babushka():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "IMG_20230707_133237.jpg")
@app.route("/Picture_bratiki")
def Picture_bratiki():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    return send_from_directory(path2, "bratiki.jpg")








@app.route("/download_chat")
def download_chat():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    body = request.get_json()["chat"]
    try:
        chat = messages[body]
    except KeyError:
        messages[body] = []
        chat = messages[body]
    for i in chat:
        if len(i) < 5:
            i.append([])
    return {"chat":chat}


@app.route("/send")
def send():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    body = request.get_json()
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    data_users_ip[body["body"][2]] = ip
    try:
        messages[body["chat"]].append(body["body"])
    except KeyError:
        messages[body["chat"]] = body["body"]
    return {1:1}


@app.route("/update")
def update():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}

    body = request.get_json()
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("update", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    messages[body["chat"]][body["num"]] = body["body"]
    return {1:1}






@app.route("/download_data")
def download_data():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    time = str(datetime.datetime.now())
    print("download_data", " ", time, " ", ip, file=ivent_data)
    ivent_data.close()
    body = request.get_json()
    if body == "333121333Aahg":
        return {"messages": messages, "files": files}
    else: return "Пороль неверный"


@app.route("/send_file", methods = ['POST'])
def send_file():
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send_file", " ", time, " ", ip, file=ivent_data)
    ivent_data.close()
    f = request.files['file']

    f.save(os.path.join(path,  f.filename.replace(':', '_')))
    return {1:1}

@app.route("/download_file")
def download_file():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    body = request.get_json()
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    time = str(datetime.datetime.now())
    print("get_file", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    return send_from_directory(path, body["filename"].replace(':', '_'))

@app.route("/delete")
def delete():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    body = request.get_json()
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr

    time = str(datetime.datetime.now())
    print("delete", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    messages[body["chat"]].pop(body["num"])
    num = 0
    if body["type"] == "text" or body["type"] == "Text":
        for i in body["files"]:
            delete_file(body["chat"], body["sender"], body["time"], num)
            num += 1
    return {1:1}


@app.route("/get_time")
def get_time():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    time = str(datetime.datetime.now())
    print("get_time", " ", time, " ", ip, file=ivent_data)
    ivent_data.close()
    tm = str(datetime.datetime.now())
    return tm


@app.route("/get_chat_java", methods = ['POST'])
def get_chat_java():
    body = request.stream.read().decode()
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")

    return_string = ""
    try:
        chat = messages[body]
        for message in chat:
            for body in message:

                if type(body) == str:
                    return_string += str(body) +"\n"
            else:
                for file in body:
                    return_string += file + ","
                return_string += "\n"
    except KeyError:
        messages[body] = []
        chat = messages[body]
    return return_string


@app.route("/send_java", methods = ['POST'])
def send_java():
    body1 = request.stream.read().decode("UTF-8")
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send_java", " ", time, " ", ip, body1 ,  file=ivent_data)
    chat, type, time, sender, text, files =  body1.split(",")
    if files != "None%&?":
        files_names = files.split("%&?")
        files_names = files_names [:-1]
    else: files_names = []
    body = {"chat":chat, "body":[type, time, sender, text, files_names]}
    try:
        messages[body["chat"]].append(body["body"])
    except KeyError:
        messages[body["chat"]] = body["body"]
    return {1: 1}


@app.route("/update_value_java", methods = ["POST"])
def update_value_java():
    body = request.stream.read().decode("UTF-8")
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send_java", " ", time, " ", ip, body, file=ivent_data)
    print(body)
    body_split = body.split(",")
    messages[body_split[0]][int(body_split[1])-1][3] = body_split[2]
    return {1:1}

@app.route("/delete_java", methods = ["POST"])
def delete_java():
    body = request.stream.read().decode("UTF-8")
    body_split = body.split(",")
    if messages[body_split[0]][int(body_split[1])][4] != []:
        num = 0
        for i in messages[body_split[0]][int(body_split[1])][4]:
            delete_file(body_split[0], messages[body_split[0]][int(body_split[1])][2], messages[body_split[0]][int(body_split[1])][1], num)
            num += 1
    messages[body_split[0]].pop(int(body_split[1]))
    return {1:1}


@app.route("/delete_chat")
def delete_chat():
    body = request.get_json()["chat"]
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("delete_chat", " ", time, " ", ip, body, file=ivent_data)
    for message in messages[body]:
        num = 0
        if message[0] == 'Text':
            if message[4] != [] and messages[body] != 0:
                for file in message[4]:
                    try:
                        delete_file(body, message[2], message[1], str(num))
                    except:
                        pass
                    num += 1
                messages[body].remove(message)
                num = 0
            if messages[body][0][4] != [] and messages[body] != 0:
                for i in messages[body][0][4]:
                    try:
                        delete_file(body, messages[body][0][2], messages[body][0][1], num)
                    except:
                        pass
                    num += 1
        elif message[0] == 'Sound':
            messages.pop(body)
        if message[0] == 'Image':
            os.remove(os.path.join(path, message[4][0].replace(":", "_")))

    messages.pop(body)
    return {1: 1}
@app.route("/delete_chat_java", methods = ["POST"])
def delete_chat_java():
    body = request.stream.read().decode("UTF-8")
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("delete_chat_java", " ", time, " ", ip, body, file=ivent_data)
    for message in messages[body]:
        num = 0
        if message[0] == 'Text':
            if message[4] != [] and messages[body] != 0:
                for file in message[4]:
                    try:
                        delete_file(body, message[2], message[1], str(num))
                    except:
                        pass
                    num += 1
                messages[body].remove(message)
                num = 0
            if messages[body][0][4] != [] and messages[body] != 0:
                for i in messages[body][0][4]:
                    try:
                        delete_file(body, messages[body][0][2], messages[body][0][1], num)
                    except:
                        pass
                    num += 1
        elif message[0] == 'Sound':
            messages.pop(body)
    messages.pop(body)

    return{1:1}

@app.route("/get_server_message")
def get_server_message():
    try:
        f = open(os.path.join(path,"server_message.txt"), 'r')
        server_message = f.read()
        f.close()
        return {1: server_message}
    except FileNotFoundError:
        print("Нет файла с серверным сообщением")
        return {1: "Нет файла с серверным сообщением"}




@app.route("/send_file_with_coding", methods = ['POST'])
def send_file_with_coding():
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send_file", " ", time, " ", ip, file=ivent_data)
    ivent_data.close()
    f = request.files['file']
    c = code.code()
    c.key.open_key_from_file(os.path.join(path, "key.k"))
    byt = f.filename.split(" ")
    byt.pop()
    byte_array = []
    for b in byt:
        byte_array.append(int(b))
    c.koded = byte_array
    c.decoding_with_open_key()
    filename = c.bytes.decode("utf-8")
    f.save(os.path.join(path,  filename.replace(':', '_')))
    return {1:1}



@app.route("/send_with_coding")
def send_with_coding():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    c = code.code()
    c.key.open_key_from_file(os.path.join(path, "key.k"))
    body_raw = request.get_json()
    c.koded = body_raw["chat"]
    c.decoding_with_open_key()
    chat = c.bytes.decode("utf-8")
    c.koded = body_raw["body"][0]
    c.decoding_with_open_key()
    type = c.bytes.decode("utf-8")
    c.koded = body_raw["body"][1]
    c.decoding_with_open_key()
    time = c.bytes.decode("utf-8")
    c.koded = body_raw["body"][2]
    c.decoding_with_open_key()
    sender = c.bytes.decode("utf-8")
    c.koded = body_raw["body"][3]
    c.decoding_with_open_key()
    text = c.bytes.decode("utf-8")
    files = []
    for file_r in body_raw["body"][4]:
        c.koded = file_r
        c.decoding_with_open_key()
        files.append(c.bytes.decode("utf-8"))
    body = [type, time, sender, text, files]


    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    time = str(datetime.datetime.now())
    print("send", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    data_users_ip[body[2]] = ip
    try:
        messages[chat].append(body)
    except KeyError:
        messages[chat] = body

    return {1:1}




@app.route("/download_file_with_coding")
def download_file_with_coding():
    ip = request.remote_addr
    if ip not in data_ips:
        data_ips.append(ip)
    if ip in black_ips:
        return {1:1}
    body = request.get_json()
    c = code.code()
    c.key.open_key_from_file(os.path.join(path, "key.k"))
    byt = body["filename"].split(" ")
    byt.pop()
    byte_array = []
    for b in byt:
        byte_array.append(int(b))
    c.koded = byte_array
    c.decoding_with_open_key()
    filename = c.bytes.decode("utf-8")
    ivent_data = open(os.path.join(path,"ivent_data.txt"), "a")
    time = str(datetime.datetime.now())
    print("get_file", " ", time, " ", ip,"", body , file=ivent_data)
    ivent_data.close()
    return send_from_directory(path, filename.replace(':', '_'))








if __name__ == '__main__':
    app.run('0.0.0.0', port=2)
is_run = False