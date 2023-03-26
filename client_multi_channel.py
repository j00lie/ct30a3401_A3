# Client side code for chat room application
# TCP-protocol used, messages Ascii encoded

import threading
import socket

nick = input("Choose a nickname: ")
channel = input("Choose a channel: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
client.connect(("127.0.0.1", 55555))  # Establish connection via three-way handshake

# Function to receive messages from the server
# Provide users nickname when prompted with "NICK"
# Provide users channel when prompted with "CHANNEL"
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nick.encode("ascii"))

            elif message == "CHANNEL":
                client.send(channel.encode("ascii"))

            elif message == "You have been disconnected.":
                print(message)
                client.close()  # close connection
                break
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = "{} ({}) : {}".format(
            nick, channel, input("")
        )  # Loop client inputs until quit command
        if message.split(": ")[1] == "quit":
            client.send("quit".encode("ascii"))
            break
        elif message.split(": ")[1].startswith("@"):
            cleaned_msg = message.split(": ")[1]
            cleaned_msg = cleaned_msg.strip("@")
            # print("CLEANED:" + cleaned_msg)
            try:
                recipient, text = cleaned_msg.split(" ", 1)
                client.send(f"@{recipient} {nick}: {text}".encode("ascii"))
            except ValueError:
                print("Enter BOTH the recipient and the message")
            except Exception as e:
                print(f"ERROR: {e}")

        else:
            client.send(message.encode("ascii"))


# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
