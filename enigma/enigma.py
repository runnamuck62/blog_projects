from collections import OrderedDict
import random


letters= [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

#These dictionaries simulate the internal wiring of the rotors and reflector
rotor1 = OrderedDict([
    ('A','Q'),
    ('B','G'),
    ('C','Z'),
    ('D','U'),
    ('E','N'),
    ('F','S'),
    ('G','V'),
    ('H','E'),
    ('I','K'),
    ('J','B'),
    ('K','X'),
    ('L','C'),
    ('M','T'),
    ('N','M'),
    ('O','A'),
    ('P','D'),
    ('Q','I'),
    ('R','R'),
    ('S','O'),
    ('T','H'),
    ('U','L'),
    ('V','Y'),
    ('W','P'),
    ('X','J'),
    ('Y','F'),
    ('Z','W')
])


rotor2 = OrderedDict([
    ('A','L'),
    ('B','A'),
    ('C','Y'),
    ('D','H'),
    ('E','G'),
    ('F','W'),
    ('G','Z'),
    ('H','T'),
    ('I','P'),
    ('J','N'),
    ('K','R'),
    ('L','C'),
    ('M','D'),
    ('N','B'),
    ('O','Q'),
    ('P','X'),
    ('Q','V'),
    ('R','O'),
    ('S','I'),
    ('T','S'),
    ('U','M'),
    ('V','F'),
    ('W','K'),
    ('X','J'),
    ('Y','E'),
    ('Z','U')
])


rotor3 = OrderedDict([
    ('A','E'),
    ('B','X'),
    ('C','M'),
    ('D','C'),
    ('E','F'),
    ('F','J'),
    ('G','U'),
    ('H','S'),
    ('I','P'),
    ('J','O'),
    ('K','G'),
    ('L','A'),
    ('M','B'),
    ('N','Z'),
    ('O','N'),
    ('P','Y'),
    ('Q','H'),
    ('R','R'),
    ('S','W'),
    ('T','L'),
    ('U','T'),
    ('V','V'),
    ('W','I'),
    ('X','K'),
    ('Y','D'),
    ('Z','Q')
])

reflector = OrderedDict([
    ('A','P'),
    ('P','A'),
    ('B','K'),
    ('K','B'),
    ('C','T'),
    ('T','C'),
    ('D','J'),
    ('J','D'),
    ('E','M'),
    ('M','E'),
    ('F','O'),
    ('O','F'),
    ('G','N'),
    ('N','G'),
    ('H','R'),
    ('R','H'),
    ('I','Y'),
    ('Y','I'),
    ('L','S'),
    ('S','L'),
    ('Q','V'),
    ('V','Q'),
    ('U','X'),
    ('X','U'),
    ('W','Z'),
    ('Z','W')
])

#The reverse wiring of the rotors for the return pass 
rotor1_inverted = {v: k for k, v in rotor1.items()}
rotor2_inverted = {v: k for k, v in rotor2.items()}
rotor3_inverted = {v: k for k, v in rotor3.items()}

ROTOR_IDX_LENGTH = 26

#Generates plugboard connections for n number of plugs
def generate_plugboard(plugs):
    plugboard = {}
    indexes = random.sample(range(0,26), plugs * 2)
    for i in range(0, plugs * 2, 2):
        k = letters[indexes[i]]
        v = letters[indexes[i+1]]
        plugboard[k] = v
        plugboard[v] = k
    return plugboard

plugboard = generate_plugboard(10)

class Enigma:
    def __init__(self, rotor_idxs, plugboard):
        self.rotors = [rotor1,rotor2,rotor3]
        self.inverted_rotors = [rotor1_inverted,rotor2_inverted,rotor3_inverted]
        self.rotor_idxs = rotor_idxs.copy()
        self.rotor_init_pos = rotor_idxs.copy()
        self.plugboard = plugboard

    #simulate the change of character when key is connected to plugboard wire
    def swap_plugboard(self, char):
        return self.plugboard.get(char,char)
    
    #simulate the turning of a rotor
    def rotate_rotor(self, rotor_number):
        self.rotor_idxs[rotor_number] = (self.rotor_idxs[rotor_number] + 1) % ROTOR_IDX_LENGTH

    #simulate the stepping of rotors when a neighbor completes a full revolution
    def step_rotors(self):
        self.rotate_rotor(0)
        if self.rotor_idxs[0] == 0:
            self.rotate_rotor(1)
            if self.rotor_idxs[1] == 0:
                self.rotate_rotor(2)

    #simulate how the character changes while passing through a rotor forwards.
    def forward_scramble(self, char, rotor_number):
        idx = letters.index(char)
        offset = idx + self.rotor_idxs[rotor_number]
        wrap = offset % 26
        char = letters[wrap]
        rotor_swapped = self.rotors[rotor_number][char]
        swapped_idx = letters.index(rotor_swapped)
        output_idx = (swapped_idx - self.rotor_idxs[rotor_number]) % 26
        rotor_final = letters[output_idx]
        return rotor_final

    #simulate how the character changes on the backwards pass of a rotor
    def reverse_scramble(self, char, rotor_number):
        idx = letters.index(char)
        offset = idx + self.rotor_idxs[rotor_number]
        wrap = offset % 26
        char = letters[wrap]
        rotor_swapped = self.inverted_rotors[rotor_number][char]
        swapped_idx = letters.index(rotor_swapped)
        output_idx = (swapped_idx - self.rotor_idxs[rotor_number]) % 26
        rotor_final = letters[output_idx]
        return rotor_final

    #full simulation of how a character changes when a button is pressed on the keyboard
    def simulate_keypress(self, char):
        char = self.swap_plugboard(char)
        char = self.forward_scramble(char,0)
        char = self.forward_scramble(char,1)
        char = self.forward_scramble(char,2)
        char = reflector[char]
        char = self.reverse_scramble(char,2)
        char = self.reverse_scramble(char,1)
        char = self.reverse_scramble(char,0)
        char = self.swap_plugboard(char)
        self.step_rotors()
        return char        
        
    def encrypt_message(self, message):
        try:
            message = message.replace(" ","").upper()
            if message.isalpha():
                encrypted_message = ''
                for char in message:
                    encrypted_char = self.simulate_keypress(char)
                    encrypted_message += encrypted_char
                return(encrypted_message)
        except:
            print("Only Letters are allowed")


enigma1 = Enigma([2,12,15,],plugboard)     
enigma2 = Enigma([2,12,15,],plugboard)

plaintext = "I SPENT WAY TOO LONG WORKING ON THIS"

encrypted = enigma1.encrypt_message(plaintext)
decrypted = enigma2.encrypt_message(encrypted)


print("Encoded Text: ",encrypted)
print("Decoded Text: ",decrypted)

           