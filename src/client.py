import socket
from game import print_hangman
import threading

def connect_to_server(host: str, port: int) -> socket.socket:
 
    socket_player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_player.connect((host,port))
    return socket_player

def thread_game(game_socket):

    server_msg = ["",""]
    
    while server_msg[0] != "end":

        server_msg = game_socket.recv(1024)
        server_msg = server_msg.decode()
        server_msg = server_msg.split("/")

        if(server_msg[0] == "nolifes"):
            print(server_msg[1])
            break
        elif(server_msg[0] == "win"):
            print(server_msg[1])
            break
        elif(server_msg[0] == "play"):
            print_hangman(server_msg[1])
            response = input("Escolha uma letra | " + "Tentativas: " + server_msg[2] + '\n')
            game_socket.send(response.encode())
        elif server_msg[0] == "wait":
            print_hangman(server_msg[1])
            print("Aguarde o outro jogador")            

def input_chat(chat_socket):
    while True:
        chat_msg = input("[CHAT]\n")
        if chat_msg.startswith("chat/"):
            chat_socket.send(chat_msg.encode())

def thread_chat(chat_socket):

    while True:
        chat_msg = chat_socket.recv(1024)
        chat_msg = chat_msg.decode()
        chat_msg = chat_msg.split("/")
        print("Mensagem do chat: " + chat_msg[1])

if __name__ == "__main__":
    game_socket = connect_to_server("127.0.0.1",12345)
    chat_socket = connect_to_server("127.0.0.1",12346)

    print("Bem vindo ao HangMan!\nComandos do jogo\nplay/letra - enviar tentativa\nchat/mensagem - enviar mensagem pelo chat\n\n")

    game_msg = game_socket.recv(1024)
    game_msg = game_msg.decode()
    game_msg = game_msg.split("/")

    if game_msg[0] == "level":
        level = input(game_msg[1])
        game_socket.send(level.encode())
    elif game_msg[0] == "wait":
        print(game_msg[1])

    chat_msg = ["",""]

    thread_chat = threading.Thread(target=thread_chat, args=(chat_socket,))
    thread_chat.start()


    while True:

        game_msg = game_socket.recv(1024)
        game_msg = game_msg.decode()
        game_msg = game_msg.split("/")

        if(game_msg[0] == "nolifes"):
            print(game_msg[1])
            break
        elif(game_msg[0] == "win"):
            print(game_msg[1])
            break
        elif(game_msg[0] == "play"):
            print_hangman(game_msg[1])
            response = input("Sua vez | " + "Letras erradas: " + game_msg[2] + '\n')
            response = response.split("/")

            if(response[0] == "chat") :
                while response[0] == "chat" :
                    chat_socket.send(response[0].encode() + "/".encode() + response[1].encode())
                    print_hangman(game_msg[1])
                    response = input("Sua vez | " + "Letras erradas: " + game_msg[2] + '\n')
                    response = response.split("/")

            response = "/".join(response)
            game_socket.send(response.encode())

        elif game_msg[0] == "wait":
            print_hangman(game_msg[1])
            response = input("Espere sua vez - digite chat/ para enviar uma mensagem ou ok/ para apenas seguir\n")
            response = response.split("/")
            if(response[0] == "chat") :
                while response[0] == "chat" :
                    chat_socket.send(response[0].encode() + "/".encode() + response[1].encode())
                    response = input("Espere sua vez - digite chat/ para enviar uma mensagem ou ok/ para apenas seguir\n")
                    response = response.split("/")
                           

    game_socket.close()
    chat_socket.close()
        

        