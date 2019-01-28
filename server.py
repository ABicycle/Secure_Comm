import socket
import asyncio
import random
from database import Data
from rsa import RSA
from Crypto.Hash import SHA256

class Server:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.crypt=RSA()
        tuple=self.crypt.prime_tuple()
        p, q = tuple
        n=p*q
        e=self.crypt.public_key(tuple)
        self.pub_k=(e, n)
        d=self.crypt.private_key(tuple, e)
        self.priv_k=(d, n)

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
        hash=SHA256.new()
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
        if res_en:
            hash.update(res_en)
            password=hash.digest()

        result=obj.check_table("users", username, password)
        if not result:
            obj.user_entry(username, password)

        await loop.sock_sendall(conn, str.encode("Enter public key: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res:
            try:
                public_key=eval(res)
            except Exception as e:
                print(str(e))

        await loop.sock_sendall(conn, str.encode("Name a group that you would want to create or join: "))
        res_en=await loop.sock_recv(conn, 2048)
        res=res_en.decode("utf-8")
        if res is not None:
            obj.create_table(res)
            key=random.randint(100000, 1000000)
            key=self.crypt.encrypt(str(key), public_key)
            await loop.sock_sendall(conn, str.encode(key))
            result=obj.check_table(res, username, password)
            if not result:
                obj.group_entry(res, username, password, key)

        conn.close()

if __name__=="__main__":
    node=Server('', 10000)
    loop=asyncio.get_event_loop()
    loop.run_until_complete(node.start(loop))