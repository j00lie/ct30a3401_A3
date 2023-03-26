# Client side code for chat room application
# TCP-protocol used, messages Ascii encoded


import threading
import socket

nick = input("Choose a nickname: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
client.connect(("127.0.0.1", 55555))  # Connect to the existing server

# Function to receive messages from the server
# Provide users nickname when prompted with "NICK"
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nick.encode("ascii"))
            else:
                print(message)
            if message == "You have been disconnected.":
                client.close()
                break
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        message = "{}: {}".format(nick, input(""))
        if message.split(": ")[1] == "quit":
            client.send("quit".encode("ascii"))
            break
        elif message.split(": ")[1].startswith("@"):
            cleaned_msg = message.split(": ")[1]
            cleaned_msg = cleaned_msg.strip("@")
            # print("CLEANED: " + cleaned_msg)
            try:
                recipient, text = cleaned_msg.split(" ", 1)
            except ValueError:
                print("Enter BOTH the recipient and the message")
            # print("RECIPIENT: " + recipient)
            # print("TEXT: " + text)
            # print(text)
            client.send(f"@{recipient} {nick}: {text}".encode("ascii"))
        else:
            client.send(message.encode("ascii"))


# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
