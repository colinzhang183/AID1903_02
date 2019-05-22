"""
    聊天室服务端
"""
from socket import *
import os, sys


# 用户登录
def load_in(sockfd, addr, msg):
    print(msg)
    if msg in guest_list:
        sockfd.sendto("该用户已存在！".encode(), addr)
    else:
        sockfd.sendto("OK".encode(), addr)
        data = "欢迎%s加入聊天室" % msg
        for item in guest_list:
            sockfd.sendto(data.encode(), guest_list[item])
        guest_list[msg] = addr


# 聊天功能
def do_chat(sockfd, name, msg):
    for item in guest_list:
        if item != name:
            data = name +":"+msg
            sockfd.sendto(data.encode(),guest_list[item])


def do_quit(sockfd,name):
    for item in guest_list:
        if item != name:
            data = name + "退出聊天."
            sockfd.sendto(data.encode(),guest_list[item])
        else:
            sockfd.sendto("EXIT".encode(),guest_list[item])
            del guest_list[item]
            sockfd.close()


def main():
    print("Waiting for connect!")
    while True:
        # 循坏等待连接
        try:
            data, addr = sockfd.recvfrom(1024)
        except KeyboardInterrupt:
            continue
        else:
            msg = data.decode().split(" ")
            if msg[0] == "L":
                load_in(sockfd, addr, msg[1])
            elif msg[0] == "C":
                text = " ".join(msg[2:])
                do_chat(sockfd, msg[1], text)
            elif msg[0] == "Q":
                do_quit(sockfd,msg[1])


if __name__ == '__main__':
    # 确定服务器地址端口
    ADDR = ("0.0.0.0", 6689)
    # 创建存储客户信息的列表,键：名称，值：客户端套接字
    guest_list = {}
    # 创建套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOCK_STREAM, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    main()
