import random
import string
import re

def generate_individuals():
    letters = list(string.ascii_uppercase)
    individuals = []
    individuals_count = 0
    while individuals_count < 100:
        indiv = list(letters)
        random.shuffle(indiv)
        if indiv not in individuals:
            individuals.append(indiv)
            individuals_count += 1
    return individuals

def print_individual():
    individuals = generate_individuals()
    print(individuals[0])

def decrypt(cryptotext,key):
    cryptotext = list(cryptotext)
    for i in range(len(cryptotext)):
        letter = cryptotext[i]
        if letter.isalpha():
            index = ord(letter) - ord('A')
            cryptotext[i] = key[index]
    return "".join(cryptotext)


def fitness(individual, cryptotext, dictionary):
    decryption = decrypt(cryptotext,individual)
    decrypted_words = re.findall("\w+", decryption)
    fitness = 0
    for word in decrypted_words:
        if word in dictionary:
            fitness += 1
    return fitness

def fitness_comparator(individual1,individual2,cryptotext,dictionary):
    if fitness(individual,cryptotext,dictionary) < fitness(individual2,cryptotext,dictionary):
        return -1
    return 0

def order_by_fitness(individuals,cryptotext,dictionary):
    ordered_individuals = sorted(individuals,key = lambda x: fitness(x,cryptotext,dictionary))
    return ordered_individuals[::-1]

def print_fitness_individuals():
    dict = ["ANA","ARE","MERE","PE","A","D","PA","NU","DA"]
    cryptotext = "MDM MRQ AQRQ Y B D C SU GF XC"
    individuals = generate_individuals()
    for indiv in individuals:
        print(fitness(indiv,cryptotext,dict),end=" ")


