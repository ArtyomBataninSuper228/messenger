import random
import math
import pickle
import requests
import copy
import time

class key:
    def __init__(self):
        self.hesh = []
        self.sdvig = random.randint(2, 8)
        self.num = random.randint(2, 15)
        self.s = random.randint(2, 15)

    def generate(self):
        for i in range(0, 256):
            a = random.randint(0, 255)
            while a in self.hesh:
                a = random.randint(0, 255)
            self.hesh.append(a)
        self.sdvig = random.randint(2, 15)
        self.num = random.randint(2, 15)

    def save_key(self, file):
        hesh = self.hesh
        hesh.append(self.sdvig)
        hesh.append(self.num)
        hesh.append(self.s)
        with open(file, 'wb') as f:
            f.write(bytes(hesh))
        f.close()
    def open_key_from_file(self, file):
        with open(file, 'rb') as f:
            h = f.read()# chatadress:[body1, body2, body3]
            hesh = []
            for i in h:
                hesh.append(int(i))
            self.sdvig = hesh[256]
            self.num = hesh[257]
            self.s = hesh[258]
            hesh.pop()
            hesh.pop()
            hesh.pop()
            self.hesh = hesh
        f.close()



class code():
    def __init__(self):
        self.key = key()
        self.bytes = []
        self.koded = []

    def coding(self):
        num_lines = math.floor(len(self.bytes)/self.key.num)
        last_line_num = len(self.bytes)%self.key.num
        if last_line_num!= 0:
            num_lines += 1
        num_byte = 0
        num_str = -1
        matrix = []
        for byte in self.bytes:
            if num_byte % self.key.num == 0:
                matrix.append([])
                num_str += 1
            matrix[num_str].append(byte)
            num_byte += 1
        self.bytes = []
        num_byte = 0
        num_str = 0
        for string in matrix:
            for byte in string:
                if num_byte%self.key.sdvig == 0 and num_str % 2 == 0 and num_str < num_lines - 2:
                    byte1 = byte
                    byte2 = matrix[num_str + 1][num_byte]
                    matrix[num_str + 1][num_byte] = byte1
                    matrix[num_str][num_byte] = byte2
                num_byte += 1
            num_str += 1
            num_byte = 0
        coding_data = []
        self.bytes = []
        num = 0
        for string in matrix:
            for byte in string:
                if num % self.key.s == 0:
                    coding_data.append(random.randint(0, 255))
                    num += 1
                num += 1
                coding_data.append(self.key.hesh[int(byte)])
        self.koded = coding_data





    def decoding(self):
        decoding_hesh = []
        for i in range(0, 256):
            decoding_hesh.append(0)
        n = 0
        for i in self.key.hesh:
            decoding_hesh[i] = n
            n += 1
        num = 0
        num_d = 0
        koded2 = []
        for i in range(0, len(self.koded)):
            if i%self.key.s !=0:
                koded2.append(self.koded[i])

        self.koded = koded2

        outp = []
        for byte in self.koded:
            outp.append(decoding_hesh[byte])
        num_lines = math.floor(len(outp) / self.key.num)
        last_line_num = len(outp) % self.key.num
        if last_line_num != 0:
            num_lines += 1
        num_byte = 0
        num_str = -1
        matrix = []
        for byte in outp:
            if num_byte % self.key.num == 0:
                matrix.append([])
                num_str += 1

            matrix[num_str].append(byte)
            num_byte += 1
        num_byte = 0
        num_str = 0
        for string in matrix:
            for byte in string:
                if num_byte%self.key.sdvig == 0 and num_str % 2 == 0 and num_str < num_lines - 2:
                    byte1 = byte
                    byte2 = matrix[num_str + 1][num_byte]
                    matrix[num_str + 1][num_byte] = byte1
                    matrix[num_str][num_byte] = byte2
                num_byte += 1
            num_str += 1
            num_byte = 0
        byt = []
        for string in matrix:
            for byte in string:
                byt.append(byte)

        self.bytes = bytes(byt)
    def open_file_bytes(self, filename):
        file = open(filename, mode="rb")
        self.bytes = file.read()
        file.close()
    def open_file_code(self, filename):
        file = open(filename, mode="rb")
        self.koded = file.read()
        file.close()

    def save_code(self, filename):
        file = open(filename, mode="wb")
        file.write(bytes(self.koded))
        file.close()
    def save_bytes(self, filename):
        file = open(filename, mode="wb")
        file.write(bytes(self.bytes))
        file.close()

    def coding_with_open_key(self):

        new_key = key()
        new_key.generate()
        new_code = code()
        new_code.key = new_key
        new_code.bytes = self.bytes
        new_code.coding()
        #koded = new_code.koded

        hesh = copy.deepcopy(new_key.hesh)
        hesh.append(new_key.sdvig)
        hesh.append(new_key.num)
        hesh.append(new_key.s)
        new_code.koded += hesh
        new_code.bytes = new_code.koded
        new_code.koded = []
        new_code.key = self.key
        new_code.coding()
        self.koded = new_code.koded
        """
        end_code = code()
        end_code.key = self.key
        end_code.bytes = new_code.koded
        end_code.coding()
        self.koded = end_code.koded
        """


    def decoding_with_open_key(self):
        end_kod = code()
        end_kod.key = self.key
        end_kod.koded = self.koded
        end_kod.decoding()

        hesh = []
        num = len(end_kod.bytes) - 259

        while(num < len(end_kod.bytes)):
            hesh.append(end_kod.bytes[num])
            num += 1


        new_key = key()
        new_key.sdvig = hesh[256]
        new_key.num = hesh[257]
        new_key.s = hesh[258]
        new_key.hesh = hesh[0:256]
        koded = []
        max_num = len(end_kod.bytes) - 260
        num = 0
        for byte in  end_kod.bytes:
            koded.append(byte)
            if num >= max_num:
                break
            num += 1
        new_code = code()
        new_code.key = new_key
        new_code.koded = koded
        new_code.decoding()
        self.bytes = new_code.bytes


'''
t1 = time.time()
c = code()
c.key.open_key_from_file("/Users/artembatanin/PycharmProjects/messenger/Server data/key.k")
c.open_file_bytes("orig.jpg")
c.coding_with_open_key()
c.decoding_with_open_key()
c.save_bytes("super.jpg")
t2 = time.time()
print(t2-t1)
'''
print("Используется Шифрование")










