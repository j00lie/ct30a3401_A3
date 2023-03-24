# TCP server for a chat room. Messages Ascii encoded

import threading
import socket

host = "127.0.0.1"
port = 55555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
server.bind((host, port))
server.listen()

clients = []
nicks = []


def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle the client connections
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message.decode("ascii") == "quit":
                index = clients.index(client)
                client.send("You have been disconnected.".encode("ascii"))
                clients.remove(client)
                client.close()
                nickname = nicks[index]
                broadcast("{} left!".format(nickname).encode("ascii"))
                nicks.remove(nickname)
                break
            elif message.decode("ascii").startswith("@"):
                # Parse the private message
                parts = message.decode("ascii").split()
                # print(parts)
                to_nickname = parts[0].strip("@")
                private_message = " ".join(parts[2:])

                # Find the recipient client and send the message
                for recipient, nickname in zip(clients, nicks):
                    if nickname == to_nickname:
                        recipient.send(
                            f"(Private from {nicks[clients.index(client)]}): {private_message}".encode(
                                "ascii"
                            )
                        )
            else:
                broadcast(message)
        except Exception as e:
            print(f"ERROR: {e}")
            break


# Function to accept new client connections
def receive():
    while True:

        # Accept the client connection
        client, address = server.accept()
        print(f"Connected with address {str(address)}")

        # Request the nickname from client and store it in the list
        client.send("NICK".encode("ascii"))
        nick = client.recv(1024).decode("ascii")
        nicks.append(nick)
        clients.append(client)

        print(f"Nickname of the client is {nick}")
        broadcast(f"{nick} joined the chat".encode("ascii"))
        client.send("Connected to the server.".encode("ascii"))

        # Create new thread for the client and use the handling function
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"Server listening at port {port}...")
receive()
