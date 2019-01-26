##Script to perform RSA encryption and decryption

import random
import math

class RSA:

    def gen_prime(self):
        prime=0
        while True:
            c=0
            a=random.randint(100, 1000)
            if not a%2==0:
                i=3
                while i*i<=a:
                    if a%i==0:
                        c+=1
                    i+=2
                if c==0:
                    prime=a
                    break
        return prime


    def prime_tuple(self):
        p=self.gen_prime()
        q=self.gen_prime()
        return (p,q)

    def totient(self, tuple):
        p, q = tuple
        return (p-1)*(q-1)

    def public_key(self, tuple):
        tot=self.totient(tuple)
        e=2
        while e<tot:
            if math.gcd(e, tot)==1:
                break
            e+=1

        return e

    def private_key(self, tuple, pub):
        tot=self.totient(tuple)
        quotient=1
        d=0
        while True:
            value=tot*quotient+1
            if value%pub==0:
                d=value/pub
                break
            quotient+=1

        return int(d)

    def encrypt(self, msg, pub_k):
        e1, n1 = pub_k
        string=""
        for i in msg:
            a=ord(i)
            a=int(pow(int(a), int(e1)))%n1
            string=string+str(a)+"#"

        return(string)

    def decrypt(self, string, priv_k):
        d, n = priv_k
        final=""
        for i in string.split("#"):
            if not i=="":
                a=int(pow(int(i), int(d)))%n        
                final=final+chr(a)

        return final



if __name__=="__main__":
    obj=RSA()
    tuple=obj.prime_tuple()
    p, q = tuple
    n=p*q
    tot=obj.totient(tuple)
    e=obj.public_key(tuple)
    pub_k=(e, n)
    d=obj.private_key(tuple, e)
    priv_k=(d, n)

    print("Public Key"+ str(pub_k))
    print("Private Key"+ str(priv_k))

    inp=input("Enter message")
    type(inp)
    choice=input("Enter choice: 1-> Encrypt, 2-> Decrypt")
    type(choice)

    if choice == "1":
        e1=input("Enter e")
        type(e1)
        n1=input("Enter n")
        type(n1)
        res=obj.encrypt(inp, (int(e1), int(n1)))
        print(res)

    else:
        res=obj.decrypt(inp, (int(d), int(n)))
        print(res)

