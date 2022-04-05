import socket
import sys
import threading


def read():
    while True:
        try:
            print(client.recv(2048).decode('utf_8'))
        except:
            client.close()
            break


def write():
    while True:
        client.send(input().encode('utf_8'))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print('2 additional arguments are expected: ip, port')
    exit()

client.connect((str(sys.argv[1]), int(sys.argv[2])))

threading.Thread(target=read).start()
threading.Thread(target=write).start()
