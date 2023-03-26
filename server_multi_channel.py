import threading
import socket

host = "127.0.0.1"
port = 55555

# Create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
server.bind((host, port))
server.listen()


# Define the list of channels and clients connected to each channel
channels = {
    "general": {"clients": [], "nicks": []},
    "programming": {"clients": [], "nicks": []},
    "gaming": {"clients": [], "nicks": []},
}

# Define a function to broadcast messages to all clients in a channel
def broadcast(channel, message):
    for client in channels[channel]["clients"]:
        client.send(message)


# Define the function to handle messages from clients in a channel
def handle(channel, client):
    while True:
        try:
            # Broadcast Messages
            message = client.recv(1024)
            # print("MESSAGE SERVER SIDE: " + message.decode("ascii"))
            if message.decode("ascii") == "quit":
                index = channels[channel]["clients"].index(client)
                client.send("You have been disconnected.".encode("ascii"))
                channels[channel]["clients"].remove(client)
                client.close()  # Close connection
                # remove nickname with corresponding client index
                nickname = channels[channel]["nicks"][index]
                broadcast(channel, "{} left!".format(nickname).encode("ascii"))
                channels[channel]["nicks"].remove(nickname)
                break
            elif message.decode("ascii").startswith("@"):
                # Parse the private message
                parts = message.decode("ascii").split()
                # print(parts)
                to_nickname = parts[0].strip("@")
                private_message = " ".join(parts[2:])

                # Find the recipient client and send the message
                for recipient, nickname in zip(
                    channels[channel]["clients"], channels[channel]["nicks"]
                ):
                    if to_nickname == nickname:
                        recipient.send(
                            f"(Private from {channels[channel]['nicks'][channels[channel]['clients'].index(client)]}): {private_message}".encode(
                                "ascii"
                            )
                        )

            else:
                broadcast(channel, message)
        except Exception as e:
            print(f"ERROR: {e}")
            break


# Define the function to accept new client connections to a channel
def receive():
    while True:
        # Accept the client connection
        (
            client,
            address,
        ) = (
            server.accept()
        )  # Establish connection with three-way handshake initiated by client
        print(f"Connected with address {str(address)}")

        # Request the nickname and channel from client and store it in the list
        client.send("NICK".encode("ascii"))
        nick = client.recv(1024).decode("ascii")

        client.send("CHANNEL".encode("ascii"))
        channel = client.recv(1024).decode("ascii")

        channels[channel]["nicks"].append(nick)
        channels[channel]["clients"].append(client)

        print(f"Nickname of the client is {nick}")
        broadcast(channel, f"{nick} joined the {channel} channel".encode("ascii"))
        client.send(f"Connected to the {channel} channel.".encode("ascii"))

        # Create new thread for the client and use the handling function
        thread = threading.Thread(target=handle, args=(channel, client,))
        thread.start()


print(f"Server listening at port {port}...")
receive()
