from collections import UserList
import threading
import socket

host = '127.0.0.1' 

port = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.bind((host, port))

server.listen()

clients = []

usernames = []

channels = []


def receive():  # For receiving new connections
    while True:
        client, address = server.accept()
        clients.append(client)

        print(f"Connected with {str(address)}")

        client.send("ABC".encode('utf-8'))

        username = client.recv(1024).decode('utf-8') ##receiving the username and adding it to a list
        usernames.append(username)
        channel = client.recv(1024).decode('utf-8')  ##receiving the channel and adding it to a list
        channels.append(channel)

        print(f"Client username: {username}\nChannel: {channel}")

        broadcast(f"{username} joined channel {channel}.".encode('utf-8'), clients.index(client))
        client.send('Connected to the server'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def broadcast(msg, index):
    channel = channels[index]
    for c in clients:
        _index = clients.index(c)
        if (channels[_index] == channel):    # Check if user is on the same channel, if not -> error message
            try:
                c.send(msg)
            except:
                print("An error occurred.")

def handle_client(client): # Handles messages
    while True:
        try:    # If receiving a message...
            message = client.recv(1024)
            decoded_message = message.decode('utf-8')
            split_message = decoded_message.split(" ")

            if (split_message[1] == "/private"): # Handling private messages
                recipientt = split_message[2]

                if recipientt in usernames:
                    index = usernames.index(recipientt)
                    recipient = clients[index]
                    decoded_message = ""

                    for i in split_message[3:]:
                        decoded_message += " " + i
                    private = ("[private] " + split_message[0] + decoded_message).encode('utf-8')

                    private_msg(recipient, private)
                else:
                    client.send("USER NOT FOUND".encode("utf-8"))
                    pass
                    ##client.send("Recipient not available.")

            #if not private message -> normal broadcast        
            else:
                index = clients.index(client)
                broadcast(message, index)


        except: # Exception for when the user disconnects.
            index = clients.index(client)
            username = usernames[index]
            clients.pop(index)
            client.close()
            broadcast(f'{username} left the chat'.encode('utf-8'), index)
            usernames.pop(index)
            channels.pop(index)
            break



print("Server running...")
receive()




# transparency, scalability, and  failure handling