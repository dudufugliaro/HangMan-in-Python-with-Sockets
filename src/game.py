def alterar_caractere(word,position,new_char):
    sword = ''.join(word)
    return sword[0:position] + new_char + sword[position+1:]

def print_hangman(hangman:str):
    for index in hangman:
        print(index + ' ',end='')
    print('')
class Game:
    def __init__(self, word, attempts):
        self.word = word
        self.attempts = attempts
        self.compare = [0] * len(word)
        self.printable_word = ''.join(['_'] * len(word))
        self.right_letters = list(set(word)) 
        self.wrong_letters = []


    def list_in_string(self) -> str:
        string = ''
        for c in self.wrong_letters:
            string += c
        return string



    def no_life(self):
        if self.attempts == 0:
            return True
        else:
            return False
    
    def winner(self):
        total = 0
        for i in range(len(self.compare)):
            total += self.compare[i]
        if total == len(self.word):
            return True
        else:
            return False
        
    def check_wrong_letter(self,letter, word):
        if letter not in word and letter not in self.wrong_letters:
            self.wrong_letters.append(letter)
        return self.wrong_letters

    def try_letter(self, character) -> str:
        #Try a character, if there is not in the word, decrease one attempt
        aux = 0
        for i in range(len(self.word)):
            if self.word[i] == character:
                self.compare[i] = 1
                aux += 1
                self.printable_word=alterar_caractere(self.printable_word,i,character)
        if aux == 0:
          self.attempts -= 1
          self.wrong_letters = self.check_wrong_letter(character,self.word)
          



# jogo = Game("banana", 3)
# while jogo.no_life() == False and jogo.winner() == False:
#     print(f"Tente acertar a palavra. Voce tem {jogo.attempts} tentativas")
#     print(f"{jogo.printable_word}")
#     c = input()
#     jogo.try_letter(c)
# print(jogo.printable_word)