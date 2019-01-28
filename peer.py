import socket
from rsa import RSA

class Peer:
    def __init__(self, addr, port):
        self.ip=addr
        self.port=port
        self.node = socket.socket()
        self.crypt=RSA()
        tuple=self.crypt.prime_tuple()
        p, q = tuple
        n=p*q
        e=self.crypt.public_key(tuple)
        self.pub_k=(e, n)
        d=self.crypt.private_key(tuple, e)
        self.priv_k=(d, n)
        print(self.pub_k)

    def connection(self):
        self.node.connect((self.ip, self.port))
        counter=0
        while True:
            query_en=self.node.recv(2048)
            if query_en:
                query=query_en.decode("utf-8")
                if query in ["Enter username: ", "Enter password: ", "Enter public key: "]:

                    response=input(query)
                    type(response)
                    self.node.sendall(str.encode(response))
                    counter+=1

            if counter==3:
                break

        message=(self.node.recv(2048)).decode("utf-8")
        if message=="Name a group that you would want to create or join: ":
            group=input(message)
            type(group)
            if group is not "":
                self.node.sendall(str.encode(group))
                data=self.node.recv(2048)
                if data:
                    encoded=data.decode("utf-8")
                    res=self.crypt.decrypt(encoded, self.priv_k)
                    print(res)
        self.node.close()

if __name__=="__main__":
    obj=Peer('', 10000)
    obj.connection()
