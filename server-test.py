import socket
import threading
import sys
import os

"""
 * sample code: https://blog.csdn.net/Olivia_2/article/details/124220255
"""


class Player:
    ip = ""
    score = 0
    fscore = 0
    matched = False

    def __init__(self, ip) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return "{ip:"+str(self.ip)+", score:"+str(self.score)+", fscore:"+str(self.fscore)+"}"

    def __repr__(self) -> str:
        return str(self)


class Config:
    default_player = Player('127.0.0.1')
    player_dict = {'127.0.0.1': default_player}


def socket_service():
    print("Waiting connection...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("137.184.236.56", 9199))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    # start to wait connection
    while True:
        conn, addr = s.accept()
        if not addr[0] in Config.player_dict.keys():
            new_player = Player(addr[0])
            Config.player_dict.update({addr[0]: new_player})
        print(Config.player_dict)
        t = threading.Thread(target=deal_data1, args=(conn, addr))
        t.start()


def deal_data1(conn, addr):
    print(f"Accept new connection from {addr}")
    data = conn.recv(1024)
    while data != "":
        file_object = open(os.path.join(
            os.getcwd(), 'server-test-file.txt'), 'rb')
        try:
            all_the_text = file_object.read()
            conn.send(str(Config.player_dict).encode())
            print("Info to client: "+str(Config.player_dict))
            print("Score data: "+data.decode())
        finally:
            file_object.close()
        # print("Waiting connection...")
        data = conn.recv(1024)


if __name__ == "__main__":
    socket_service()
