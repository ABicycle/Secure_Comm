import socket
import asyncio
import random
from database import Data

class Server:
    def __init__(self, host, port):
        self.host=host
        self.port=port

    async def start(self, loop):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serv.bind((self.host,self.port))
            serv.setblocking(False)
            print("server started...")
        except socket.error as e:
            print(str(e))

        serv.listen()

        while True:
            conn , addr = await loop.sock_accept(serv)
            print(str(addr)+" connected")
            loop.create_task(self.handler(conn, loop))

    async def handler(self, conn, loop):
        obj=Data()
        username=""
        password=""
        public_key=""
        await loop.sock_sendall(conn, str.encode("Enter username: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res:
            username=res
        await loop.sock_sendall(conn, str.encode("Enter password: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res:
            password=res

        result=obj.check_table("users", username, password)
        if not result:
            obj.user_entry(username, password)

        await loop.sock_sendall(conn, str.encode("Enter public key: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res:
            public_key=res

        await loop.sock_sendall(conn, str.encode("Name a group that you would want to create or join: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res is not None:
            obj.create_table(res)
            key=random.randint(100000, 1000000)
            await loop.sock_sendall(conn, str.encode(str(key)))
            result=obj.check_table(res, username, password)
            if not result:
                obj.group_entry(res, username, password, key)

        conn.close()

if __name__=="__main__":
    node=Server('', 10000)
    loop=asyncio.get_event_loop()
    loop.run_until_complete(node.start(loop))