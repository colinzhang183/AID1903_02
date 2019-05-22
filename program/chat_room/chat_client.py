"""
    聊天室客户端
"""
from socket import *
import os, sys


def do_quit(sockfd, name):
    data = "Q %s" % name
    sockfd.sendto(data.encode())


def send_msg(sockfd, name):
    while True:
        msg = input(">>\n")
        if msg == "quit":
            do_quit(sockfd, name)
            return
        data = "C %s %s" % (name, msg)
        sockfd.sendto(data.encode(), ADDR)


def get_msg(sockfd):
    while True:
        data, addr = sockfd.recvfrom(4096)
        if data.decode() == "EXIT":
            sys.exit("退出聊天室")
        print(data.decode())


def main():
    # 创建客户端套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入登录名称：")
        sockfd.sendto(("L " + name).encode(), ADDR)
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == "OK":
            print("登录成功,现在可以开始聊天了.")
            break
        print(data.decode())

    # 接收消息和发送消息分离 创建多进程
    pid = os.fork()

    if pid < 0:
        os._exit(0)
    elif pid == 0:
        # 子进程接收消息
        get_msg(sockfd)
        sockfd.close()
        return
    else:
        # 父进程发送消息
        send_msg(sockfd, name)



if __name__ == '__main__':
    # 确定服务器端口
    ADDR = ("127.0.0.1", 6689)
    main()
