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
        initial_text = list(fd.read().upper())
    for i in range(len(initial_text)):
        letter = initial_text[i]
        if letter.isalpha():
            index = ord(letter) - ord('A')
            initial_text[i] = encryption_rule[index]
    return "".join(initial_text)

def build_dictionary():
    with open("dictionary_input.txt","r",encoding='utf-8') as fd:
        input_dictionary = set(re.findall("\w+", fd.read().upper()))
    return input_dictionary

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

def print_fitness_individuals():
    dict = ["ANA","ARE","MERE","PE","A","D","PA","NU","DA"]
    cryptotext = "MDM MRQ AQRQ Y B D C SU GF XC"
    individuals = generate_individuals()
    for indiv in individuals:
        print(fitness(indiv,cryptotext,dict),end=" ")


def order_by_fitness(individuals,cryptotext,dictionary):
    ordered_individuals = sorted(individuals,key = lambda x: fitness(x,cryptotext,dictionary))
    ordered_individuals = ordered_individuals[::-1]
    fitness_sum = sum(fitness(x,cryptotext,dictionary) for x in ordered_individuals)
    individuals_with_fitness = []
    for individual in ordered_individuals:
        fi = fitness(individual,cryptotext,dictionary)/fitness_sum
        individuals_with_fitness.append((individual,fi))
    return individuals_with_fitness

def get_individuals_roulette(individuals):
    individuals_roulette = []
    i = 0
    while len(individuals_roulette) < 100:
        individual = individuals[i]
        fitness = individual[1]
        importance = max(int(fitness * 100),1)
        current_length = len(individuals_roulette)
        for count in range(current_length,current_length+importance):
            individuals_roulette.append(i)
        i += 1
    return individuals_roulette

def spin_roulette(individuals,roulette):
    random_individual_index = random.randint(0,99)
    return individuals[roulette[random_individual_index]]

def cross_over(individual1,individual2):
    split_index = random.randint(1,24)
    child1 = individual1[0:split_index]
    child1.extend(individual2[split_index:25])
    child2 = individual2[0:split_index]
    child2.extend(individual1[split_index:25])
    #childs = solve_conflicts(child1,child2)
    return (child1,child2)

def mutation(individual):
    index1 = random.randint(0,25)
    index2 = random.randint(0,25)
    letter1 = individual[index1]
    letter2 = individual[index2]
    individual[index1] = letter2
    individual[index2] = letter1
    return individual

def solve():
    cryptotext = encryption()
    dictionary = build_dictionary()
    individuals = generate_individuals()
    ordered_individuals = order_by_fitness(individuals, cryptotext, dictionary)
    turnir_winner = turnir(ordered_individuals)
    print (turnir_winner)
    roulette = get_individuals_roulette(ordered_individuals)
    rand_ind1 = spin_roulette(individuals,roulette)
    rand_ind2 = spin_roulette(individuals,roulette)
    childs = cross_over(rand_ind1,rand_ind2)
    child1 = childs[0]
    child2 = childs[1]
    x = 2

def scor_turnir(individual):
    fitness_weight  = 0.7
    random_bonus_weight = 0.3
    random_bonus = random.random()
    scor = individual[0][1] * fitness_weight + random_bonus * random_bonus_weight
    return scor

def winner(individual_1, individual_2):
    if scor_turnir(individual_1) > scor_turnir(individual_2):
        return individual_1
    else:
        return individual_2

def fight_turnir(individuals_1, individuals_2):
    if len(individuals_1) <= 1 and len(individuals_2) <= 1:
        return winner(individuals_1, individuals_2)
    else:
        return fight_turnir(fight_turnir(individuals_1[0:len(individuals_1)//2], individuals_1[len(individuals_1)//2:],),
                            fight_turnir(individuals_2[0:len(individuals_2)//2], individuals_2[len(individuals_2)//2:],))

def turnir(individuals):
    random.shuffle(individuals)
    n = random.choice([2, 4, 8, 16, 32, 64])
    top_n_individuals = individuals[0:n]
    turnir_winner = fight_turnir(top_n_individuals[0:n//2], top_n_individuals[n//2:n])
    return turnir_winner

solve()

