import random

def read_and_return_word(arquivo):
   
    with open(arquivo, 'r') as file:
       
        words = file.read()
        palavras = words.split(',')
    
    return random.choice(palavras)
