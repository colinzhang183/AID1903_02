"""
    http_server2.0
    技术点：1.服务器封装成类
           2.采用tcp套接字进行通信
           3.采用IO多路复用中的selec方法处理
"""
from socket import *
from select import select


# 创建服务器类进行属性封装
class HttpServer:
    def __init__(self, ADDR, dir_target):
        self.addr = ADDR
        self.dir_target = dir_target
        self.rlist = []  # 创建select列表
        self.wlist = []
        self.xlist = []
        self.create_socket()  # 创建套接字
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOCK_STREAM, SO_REUSEADDR, 1)  # 设置端口立即复用
        self.rlist.append(self.sockfd)

    def bind(self):
        self.sockfd.bind(self.addr)
        self.ip = self.addr[0]
        self.port = self.addr[1]

    def request(self):
        self.sockfd.listen(5)
        print("Listen the port %d." % self.port)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r == self.sockfd:
                    c, addr = r.accept()
                    print("Connect from:" , addr)
                    self.rlist.append(c)
                else:
                    data = r.recv(4096)
                    if not data:
                        r.close()
                        self.rlist.remove(r)
                        continue
                    self.handle(r,data)

    def handle(self,c,data):
        msg = data.splitlines()[0].decode()
        info = msg.split(" ")[1]
        if info == "/" or info[-5:] == ".html":
            self.get_html(c,info)
        else:
            self.get_data(c)

    def get_html(self,c,info):
        filename = self.dir_target + info
        if info == "/":
            filename = self.dir_target + "/index.html"
        try:
            fd = open(filename)
        except:
            respnse = "HTTP/1.1 400 Not Found\r\n"
            respnse += "Content-Type:text/html\r\n"
            respnse += "\r\n"
            respnse += "<h1>Sorry,Not Found!</h1>"
            c.send(respnse.encode())
        else:
            respnse = "HTTP/1.1 200 OK\r\n"
            respnse += "Content-Type:text/html\r\n"
            respnse += "\r\n"
            respnse += fd.read()
            c.send(respnse.encode())

            fd.close()


    def get_data(self,c):
        respnse = "HTTP/1.1 200 OK\r\n"
        respnse += "Content-Type:text/html\r\n"
        respnse += "\r\n"
        respnse += "<h1>To be Continue!</h1>"
        c.send(respnse.encode())




def main():
    # 传递服务器地址和目标路径
    ADDR = ("0.0.0.0", 8866)
    dir_target = "./target"
    # 生成服务器对象
    hs = HttpServer(ADDR, dir_target)
    hs.request()


if __name__ == '__main__':
    main()
