
##  Santeri Ruuskanen 0567818
##  Distributed Systems assignment 1 070322


##  Sources:
##  https://www.youtube.com/watch?v=3UOyky9sEQY&t=414s
##  https://docs.python.org/3.9/library/socket.html
##  https://docs.python.org/3.9/library/threading.html


import threading
import socket



host = '127.0.0.1' #localhost
port = 4000

username = input("Username: ")
channel = input("Channel: ")

print("Welcome to the chat room, for private messages use format '/private recipient message'.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((host, port))

def write_message():
    while True:
        message_input = input("")
        message = f'{username}: {message_input}'
        client.send(message.encode("utf-8"))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "ABC":
                client.send(username.encode("utf-8"))
                client.send(channel.encode("utf-8"))
                pass
            elif message == "USER NOT FOUND":
                print("Private message recipient not found, try again! \n\n")
                pass

                
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


##    /private name message


##defining and running threads
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
write_thread = threading.Thread(target=write_message)
write_thread.start()