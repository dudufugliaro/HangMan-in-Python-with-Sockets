import socket
from file import read_and_return_word
from game import Game
import threading
import random

def start_server(host: str, port: int) -> socket.socket:

    #inicializa um socket TCP (de fluxo) de "escuta"
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #define o IP que ira receber comunicacoes e a porta associada
    socket_server.bind((host,port))
    #define o socket como de escuta e define 2 como o numero maximo de conexoes pendentes
    socket_server.listen(2)

    return socket_server

def thread_game(socket_p1,socket_p2,flag,game):

    while game.no_life() == False and game.winner() == False :

        wrong_letters = game.list_in_string()

        if flag == 0 :
                
            socket_p1.send("play/".encode() + game.printable_word.encode() + "/".encode() + wrong_letters.encode())
            socket_p2.send("wait/".encode() + game.printable_word.encode() + "/".encode() + wrong_letters.encode())
            response = socket_p1.recv(128)
            response = response.decode()
            response = response.split("/")
            game.try_letter(response[1])
            flag = 1

        else :
            socket_p1.send("wait/".encode() + game.printable_word.encode() + "/".encode() + wrong_letters.encode())
            socket_p2.send("play/".encode() + game.printable_word.encode() + "/".encode() + wrong_letters.encode())
            response = socket_p2.recv(128)
            response = response.decode()
            response = response.split("/")
            game.try_letter(response[1])
            flag = 0
        
        if game.no_life():

            socket_p1.send("nolifes/Acabaram as chances :(".encode())
            socket_p2.send("nolifes/Acabaram as chances :(".encode())
            break
        if game.winner() and flag == 1:
            socket_p1.send("win/".encode() + "Boa! Ganhou :)/".encode() + game.printable_word.encode() )
            socket_p2.send("win/".encode() + "Triste! Perdeu :(/".encode() + game.printable_word.encode() )
            break
        elif game.winner() and flag == 0:
            socket_p2.send("win/".encode() + "Boa! Ganhou :)/".encode() + game.printable_word.encode() )
            socket_p1.send("win/".encode() + "Triste! Perdeu :(/".encode() + game.printable_word.encode() )
            break

def thread_chat(socket_p1,socket_p2):

    socket_p1.send("chat/CHAT INICIADO".encode())
    while True:
        player_msg = socket_p1.recv(1024)
        player_msg = player_msg.decode()
        socket_p2.send(player_msg.encode())




if __name__ == "__main__":
    choice_player = random.randint(0,1)

    game_socket_server = start_server('127.0.0.1',12345)
    print("Aguardando jogadores pro jogo...")
    chat_socket_server = start_server('127.0.0.1',12346)
    print("Aguardando jogadores pro chat...")

    game_socket_player1, game_adress_player1 = game_socket_server.accept()
    print("Jogador 1 conectado ao servidor do jogo")
    chat_socket_player1, chat_adress_player1 = chat_socket_server.accept()
    print("Jogador 1 conectado ao servidor do chat")

    game_socket_player2, game_adress_player2 = game_socket_server.accept()
    print("Jogador 2 conectado ao servidor do jogo")
    chat_socket_player2, chat_adress_player2 = chat_socket_server.accept()
    print("Jogador 2 conectado ao servidor do chat")
    

    if choice_player == 0:
        game_socket_player1.send("level/Escolha uma dificuldade (easy,medium,hard)/null".encode() )
        game_socket_player2.send("waitlevel/O outro jogador vai escolher a dificuldade/null".encode()) #ALTEREI
        level = game_socket_player1.recv(124)
        level = level.decode()
        level = level.split("/")  #ALTEREI
        hangman = read_and_return_word(level[1])  #ALTEREI
    else:
        game_socket_player2.send("level/Escolha uma dificuldade (easy,medium,hard)/null".encode())
        game_socket_player1.send("waitlevel/O outro jogador vai escolher a dificuldade/null".encode())  #ALTEREI
        level = game_socket_player2.recv(124)
        level = level.decode()
        level = level.split("/")    #ALTEREI
        hangman = read_and_return_word(level[1])  #ALTEREI
  
    game = Game(hangman,6)

    print(game.word)

    thread_game = threading.Thread(target=thread_game, args=(game_socket_player1,game_socket_player2,choice_player,game))
    thread_game.start()
    
    thread_chat_player1 = threading.Thread(target=thread_chat, args=(chat_socket_player1,chat_socket_player2))
    thread_chat_player2 = threading.Thread(target=thread_chat, args=(chat_socket_player2,chat_socket_player1))
    thread_chat_player1.start()
    thread_chat_player2.start()

    game_socket_player1.close()
    game_socket_player2.close()
    chat_socket_player1.close()
    chat_socket_player2.close()




