import socket
import threading
from tkinter import * 
from desenhos import *
from playsound import playsound


def format_text_forca(text: str) -> str:
    return ' '.join(text)


class Aplication:
    def __init__(self):
        self.wrong_letters = ["",""]
        self.attempts = 6
        self.printable_word = ""
        self.root = Tk()
        self.chat_socket = None
        self.game_socket = None
        self.game_msg = None
        self.chat_msg = None
        self.initialize_sockets()

        # Gera tela
        self.tela()
        # Configura tela
        self.frames_da_tela()
        # Gera e configura forca
        self.forca(format_text_forca(self.printable_word), get_desenhos_forca(self.attempts))
        # Gera botoes da forca
        self.buttons()

        # Inicia as threads para o jogo e para o chat
        self.start_threads()

        # Inicia o loop principal da interface
        self.root.mainloop()
    
    def start_threads(self):
        """Inicia as threads para o jogo e chat"""
        self.thread_game = threading.Thread(target=self.handle_game_messages)
        self.thread_game.start()
        self.thread_chat = threading.Thread(target=self.handle_chat_messages)
        self.thread_chat.start()

    def initialize_sockets(self):
        """Inicializa os sockets de jogo e chat"""
        self.game_socket = self.connect_to_server("192.168.246.113", 12345)
        self.chat_socket = self.connect_to_server("192.168.246.113", 12346)

    def connect_to_server(self, host: str, port: int) -> socket.socket:
        """Conecta ao servidor de jogo ou chat"""
        socket_player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_player.connect((host, port))
        return socket_player


    def handle_game_messages(self):
        
        tmp_error = 10

        while True:
            game_msg = self.game_socket.recv(1024).decode().split("/")
            self.game_msg = game_msg[1]
            self.update_labels()

            if game_msg[0] == "nolifes":
                self.attempts = 0
                self.update_labels()
                break
            elif game_msg[0] == "win":
                self.game_msg = game_msg[1]

                if "Ganhou"  in game_msg[1]:
                    playsound('Vitoria.mp3')
                elif "Perdeu" in game_msg[1]:
                    playsound('Derrota.mp3')

                self.printable_word = game_msg[2]
                self.update_labels()
                break

            if tmp_error < len(list(game_msg[2])):
                playsound('Erro.mp3')
            elif tmp_error != 10 and tmp_error == len(list(game_msg[2])):
                playsound('Aceerto.mp3')
    
            if game_msg[0] == "play":
                # Atualiza o estado do jogo na interface
                self.game_msg = "Sua vez"
                self.wrong_letters = list(game_msg[2])
                self.attempts = len(self.wrong_letters)
                tmp_error = self.attempts
                self.printable_word = game_msg[1]
            elif game_msg[0] == "wait":
                self.game_msg = "Espere sua vez - digite chat/ para enviar uma mensagem no chat\n"
                self.wrong_letters = list(game_msg[2])
                self.attempts = len(self.wrong_letters)
                tmp_error = self.attempts
                self.printable_word = game_msg[1]
            elif game_msg[0] == "levelwait":
                self.game_msg = game_msg[1]

            self.update_labels()

        self.game_socket.close()
        self.chat_socket.close()
    
    def handle_chat_messages(self):
        while True:
            chat_msg = self.chat_socket.recv(1024).decode().split("/")
            if chat_msg[0] == "chat":
                self.chat_msg = chat_msg[1]
                self.update_labels()
    
    def button_try(self):
        txt = self.txt_confirm.get()
        self.txt_confirm.delete(0, END)
        txt = txt.split("/")

        while(txt[0] == "chat"):
            self.chat_socket.send("/".join(txt).encode())
            txt = self.txt_confirm.get()
            self.txt_confirm.delete(0, END)
            txt = txt.split("/")
            
        
        # if txt[0] != "ok" :
        txt = "/".join(txt)
        self.game_socket.send(txt.encode())

    def send_chat_message(self, msg):
        self.chat_socket.send(msg.encode())

    def tela(self):
        self.root.title("Jogo da Forca")
        self.root.geometry("1080x720")
    
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4)
        self.frame_1.place(relx=0.07, rely=0.04, relwidth=0.85, relheight=0.6)
        self.frame_2 = Frame(self.root, bd=4)
        self.frame_2.place(relx=0.07, rely=0.8, relwidth=0.85, relheight=0.1)

        self.lb_info_game = Label(self.frame_1, text="Comandos para jogar\nlevel/+texto - responder dificuldade\nplay/+letra - responder jogada\n chat/+texto - enviar mensagem pelo chat\n ", font=("Consolas", 15))
        self.lb_info_game.place(relx=0.50, rely=0.1)

        self.lb_game_msg = Label(self.frame_2, text="Servidor do jogo:", font=("Consolas", 15))
        self.lb_game_msg.place(relx=0.05, rely=0.6)
        self.chat_label = Label(self.root, text="CHAT:", font=("Consolas", 12), anchor="w", justify="left")
        self.chat_label.place(relx=0.07, rely=0.65, relwidth=0.85, relheight=0.1)
    
    def forca(self, word, attempts):
        self.lb_forca = Label(self.frame_1, text=attempts, font=("Consolas", 40), justify="left")
        self.lb_forca.place(relx=0.05, rely=0.05)

        self.lb_word = Label(self.frame_1, text=word, font=("Consolas", 30), justify="left")
        self.lb_word.place(relx=0.4, rely=0.8)

    def buttons(self):
        self.bt_confirm = Button(self.frame_2, text="Enviar", command=self.button_try)
        self.bt_confirm.place(relx=0.20, rely=0.05, relheight=0.40, relwidth=0.08)  

        self.lb_confirm = Label(self.frame_2, text="Resposta:")
        self.lb_confirm.place(relx=0.03, rely=0.05, relheight=0.4)
        
        self.txt_confirm = Entry(self.frame_2, validate="key", validatecommand=(self.root.register(self.validaCaractere), '%P'))
        self.txt_confirm.place(relx=0.1, rely=0.05, relheight=0.4, relwidth=0.1)

        self.lb_wrong_letters = Label(self.frame_2, text="LETRAS ERRADAS:")
        self.lb_wrong_letters.place(relx=0.35, rely=0.05)
   
    def update_labels(self):
        self.lb_forca.config(text=get_desenhos_forca(self.attempts))
        self.lb_word.config(text=format_text_forca(self.printable_word))
        pre_phrase = "LETRAS ERRADAS: "
        self.lb_wrong_letters.config(text=pre_phrase + ''.join((self.wrong_letters)))
        self.lb_game_msg.config(text=f"Mensagens do jogo: {self.game_msg}")
        self.chat_label.config(text=f"CHAT: {self.chat_msg}")

    def disable_widgets(self):
        self.lb_word.config(text=format_text_forca(self.printable_word))
        self.lb_confirm.place_forget()
        self.txt_confirm.place_forget()
        self.bt_confirm.place_forget()

    def validaCaractere(self, text):
        return len(text) <= 20


Aplication()
