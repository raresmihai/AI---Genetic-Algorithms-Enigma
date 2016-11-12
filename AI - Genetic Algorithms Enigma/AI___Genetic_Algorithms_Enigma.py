import random
import string
import re

def output(initial_text, encrypted_text, encryption_rule):
    print("Text before encryption is {0}".format(initial_text))
    print("Text after encryption is {0}".format(encrypted_text))
    print("The encryption rule applied is {0}".format(encryption_rule))

def encryption():
    encryption_rule = list(string.ascii_uppercase)
    random.shuffle(encryption_rule)
    with open("text_to_be_encrypted.txt") as fd:
        initial_text = re.findall("\w+", fd.read().upper())
    encrypted_text = ""
    for word in initial_text:
        for i in range(0,len(word)):
            encrypted_text += encryption_rule[ord(word[i])-65]
    output(initial_text, encrypted_text, encryption_rule)
    return encrypted_text

def build_dictionary():
    with open("dictionary_input.txt") as fd:
        input_dictionary = set(re.findall("\w+", fd.read().upper()))
    return input_dictionary

