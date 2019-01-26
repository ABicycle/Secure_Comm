# Secure_Comm

Implementing secure communication over LAN.

## Stages

* The peer connects to the server.
* The server asks for authentification. If the peer is a new user, he gets added to the users database.
* Everytime the peer logs in, it is asked whether it wants to join or create any new chat rooms. Based on its availability, the chat rooms are created or the peer gets added to the room_members' database.

## Documentation

#### rsa.py
* **RSA** -> Main class which contains methods for encryption and decryption.
* **gen_prime()** -> Generates a prime number in a range.
* **prime_tuple()** -> Generates a prime tuple by calling gen_prime().
* **totient(tuple)** -> Calculate phi(x*y) where (x,y) is the prime_tuple and phi() is the Euler's Totient Function.
* **public_key(tuple)** -> Calculate the public_key which is visible globally.
* **private_key(tuple, pub)** -> Calculate the private key using the public key.
* **encrypt(msg, pub_k)** -> Encrypt a message using the recipient's public key.
* **decrypt(string, priv_k)** -> Decrypt an encrypted message using own's private key.

#### server.py
* **Server** -> Main Server class used to initialize the server using the host ip address and port number specified by the user. The server asynchronously manages many clients.
* **start(loop)** -> Starts the server, which handles every client asynchronously.
* **handler(conn, loop)** -> The handling function for every client, having the connection object as an argument. Performs functions like authentification. **Improvement required - Should effectively support group chats and personal chats**


#### peer.py
* **Peer** -> Main class which initializes the peer node providing it with the ip address and port of the server to connect to.
* **connection** -> Handles the interations between the server and the peers.

#### database.py
* **Data** -> Main database class.
* **create_table(name)** -> Creates a table in the database if it does not exist already.
* **check_table(name)** -> Checks the table for user authentification, returning a boolean value.
* **read_table(name)** -> Reads the contents of a table and displays the results to the console.
* **user_entry(username, password)** -> Used to enter the user data to the `users` database.
* **group_entry(group_name, username, password, key)** -> Used to enter the user data to a group, along with a random key specified by the server.

##Improvements to be done
* Implementing chat section.
* Encrypting passwords.
* RSA encryption and decryption is a quite time consuming process. Need to manage every chat message, efficiently breaking it into chunks, and performing RSA algorithms on them concurrently, to speed up the process.

**This is just the begining phase of this project. Further improvements will take place soon.**
