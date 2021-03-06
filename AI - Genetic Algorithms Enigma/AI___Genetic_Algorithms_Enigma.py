import random
import string
import re

def output_encryption_rule(fd,encryption_rule):
    for i in range(len(encryption_rule)):
        fd.write("{0}->{1} ".format(chr(i+65),encryption_rule[i]))
    fd.write("\n\n")

def output(initial_text, encrypted_text, encryption_rule):
    with open("solution.txt","w") as fd:
        fd.write("Text before encryption is \n{0}\n\n".format(initial_text))
        fd.write("Text after encryption is \n{0}\n\n".format(encrypted_text))
        #output_encryption_rule(fd,encryption_rule)
        fd.write("The encryption rule applied is \n{0}\n\n".format(encryption_rule))
    

def encryption():
    encryption_rule = list(string.ascii_uppercase)
    random.shuffle(encryption_rule)
    encryption_key = encryption_rule
    with open("text_to_be_encrypted.txt") as fd:
        initial_text_copy = fd.read().upper()
        initial_text = list(initial_text_copy)
        
    for i in range(len(initial_text)):
        letter = initial_text[i]
        if letter.isalpha():
            index = ord(letter) - ord('A')
            initial_text[i] = encryption_rule[index]
    encryption = "".join(initial_text)
    output(initial_text_copy,encryption,encryption_rule)
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
    #output_generare_indivizi(individuals)
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
            if index > len(key):
                print (index)
            cryptotext[i] = key[index]
    return "".join(cryptotext)


def fitness(individual, cryptotext, dictionary):
    decryption = decrypt(cryptotext,individual)
    decrypted_words = re.findall("\w+", decryption)
    fitness = 0
    found_words = []
    for word in decrypted_words:
        if word in dictionary and word not in found_words:
            found_words.append(word)
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
    fitness_sum = max(sum(fitness(x,cryptotext,dictionary) for x in ordered_individuals),1)
    individuals_with_fitness = []
    for individual in ordered_individuals:
        original_fitness = fitness(individual,cryptotext,dictionary)
        normalized_fitness = original_fitness/fitness_sum
        individuals_with_fitness.append((individual,normalized_fitness,original_fitness))
    #output_evaluare_fitness_si_ordonare(individuals_with_fitness)
    return individuals_with_fitness

def onlyOneFitness(individuals):
    if individuals[0][1] == 0:
        return False
    i = 0
    while i < 98 and individuals[i][1] == individuals[i+1][1]:
        i += 1
    if individuals[i+1][1] == 0 and i < 4:
        return True
    return False


    
def get_individuals_roulette(individuals):
    individuals_roulette = []
    i = -1
    if onlyOneFitness(individuals):
        for count in range (30):
            individuals_roulette.append(i)
            if count % 10 == 0:
                i += 1
        for count in range(70):
            individuals_roulette.append(i)
            i += 1
    else:
        i = 0
        while len(individuals_roulette) < 100:
            individual = individuals[i]
            fitness = individual[1]
            importance = max(int(fitness * 100),1)
            current_length = len(individuals_roulette)
            for count in range(current_length,current_length+importance):
                individuals_roulette.append(i)
            i += 1
    #if individuals[0][2] != 0:
        #output_ruleta(individuals,individuals_roulette)
    return individuals_roulette

def spin_roulette(individuals,roulette):
    random_individual_index = random.randint(0,99)
    #output_castigatorul_ruletei(individuals, random_individual_index)
    return individuals[roulette[random_individual_index]]

def cross_over(individual1,individual2):
    split_index = random.randint(1,24)
    child1 = individual1[0:split_index]
    child1.extend(individual2[split_index:26])
    child2 = individual2[0:split_index]
    child2.extend(individual1[split_index:26])
    childs = solve_conflicts(child1,child2)
    #output_cross_over(individual1,individual2,child1,child2,split_index)
    return childs

def solve_conflicts(child1,child2):
    #child1 = ["5","4","8","5","8","9","2","1","6"]
    #child2 = ["7","3","4","9","7","1","2","3","6"]
    child1_index_duplicates = []
    child1_letter_duplicates = []
    child2_index_duplicates = []
    child2_letter_duplicates = []
    for i in range(len(child1)):
        letter = child1[i]
        if child1.count(letter) > 1 and letter not in child1_letter_duplicates:
            child1_index_duplicates.append(i)
            child1_letter_duplicates.append(letter)
    for i in range(len(child2)):
        letter = child2[i]
        if child2.count(letter) > 1 and letter not in child2_letter_duplicates:
            child2_index_duplicates.append(i)
            child2_letter_duplicates.append(letter)

    for i in range(len(child1_index_duplicates)):
        child1_duplicate_index = child1_index_duplicates[i]
        child1_duplicate_letter = child1_letter_duplicates[i]
        child2_duplicate_index = child2_index_duplicates[i]
        child2_duplicate_letter = child2_letter_duplicates[i]
        child1[child1_duplicate_index] = child2_duplicate_letter
        child2[child2_duplicate_index] = child1_duplicate_letter
    return (child1,child2)
    
def mutation(individual):
    individual_copy = list(individual)
    index1 = random.randint(0,25)
    index2 = random.randint(0,25)
    letter1 = individual_copy[index1]
    letter2 = individual_copy[index2]
    individual_copy[index1] = letter2
    individual_copy[index2] = letter1
    return individual_copy

def get_elite(ordered_individuals):
    return [individual[0] for individual in ordered_individuals[0:6]]

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
    mutation1 = mutation(rand_ind1)
    mutation2 = mutation(rand_ind2)
    roulette_winners = get_winners_from_roulette(ordered_individuals)
    childs = get_childs_from_cross_over(roulette_winners)
    x = 2

def scor_turnir(individual):
    fitness_weight  = 0.7
    random_bonus_weight = 0.3
    random_bonus = random.random()
    scor = individual[0][1] * fitness_weight + random_bonus * random_bonus_weight
    return scor

def winner(individual_1, individual_2):
    #output_winner_turnir(individual_1, individual_2, scor_turnir(individual_1), scor_turnir(individual_2))
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


def get_winners_from_turnir(individuals):
    individuals_copy = list(individuals)
    turnir_winners = []
    for i in range(0, 30):
        turnir_winner = turnir(individuals_copy)
        turnir_winners.append(turnir_winner[0][0])
    return turnir_winners

def get_childs_from_mutations(individuals):
    childs = []
    for individual in individuals:
        mutationn = mutation(individual)
        childs.append(mutationn)
    return childs

def last_best_individual_still_first(last_best_individual,individuals):
    i = 0
    if last_best_individual == individuals[0][0]:
        return True
    while i < len(individuals)-1 and individuals[i][1] == individuals[i+1][1]:
       i += 1
       if last_best_individual == individuals[i][0]:
           return True
    return False

def count_number_of_unique_words(cryptotext):
    words = re.findall("\w+", cryptotext)
    sol = len(set(words))
    return sol

def find_cypher():
    cryptotext = encryption()
    number_of_words = count_number_of_unique_words(cryptotext)
    print(number_of_words)
    dictionary = build_dictionary()
    individuals = generate_individuals()
    individuals = order_by_fitness(individuals,cryptotext,dictionary)
    number_of_epochs = 100
    last_best_individual_fitness = 0
    unchanged = 0
    childs = []
    restart = 20

    while True:
        childs = []
        childs.extend(get_elite(individuals))
        turnir_winners = get_winners_from_turnir(individuals)
        roulette_winners = get_winners_from_roulette(individuals)
        childs.extend(get_childs_from_mutations(turnir_winners))
        childs.extend(get_childs_from_cross_over(roulette_winners))
        individuals = order_by_fitness(childs,cryptotext,dictionary)
        if last_best_individual_fitness == individuals[0][2]:
            unchanged += 1
        else:
            last_best_individual_fitness = individuals[0][2]
            unchanged = 0

        if unchanged > number_of_epochs or individuals[0][2] == number_of_words:
            break

        if unchanged > restart and individuals[0][2] < number_of_words/5:
                individuals = generate_individuals()
                individuals = order_by_fitness(individuals,cryptotext,dictionary) 

        print ("",last_best_individual_fitness)
        print (individuals[0])
        print (individuals[1])
        print (individuals[2])
        print (individuals[3])
        print (individuals[4])
        print (individuals[5])
        print (individuals[6])
        print (individuals[7])
        print ("unchanged=",unchanged)
        print ("------------------------------------------")
        if unchanged == number_of_epochs:
            break

    decryption_key = individuals[0][0]

    decryption = decrypt(cryptotext,decryption_key)
    with open("solution.txt","a") as fd:
        fd.write(str(build_encryption_key_from_decryption_key(decryption_key)))
        fd.write("\n")
        #fd.write(str(decryption_key))
        fd.write("\n")
        fd.write(decryption)

def get_winners_from_roulette(individuals):
    roulette_winners = []
    roulette = get_individuals_roulette(individuals)
    for count in range(64):
        roulette_winner = spin_roulette(individuals,roulette)
        if roulette_winner[0] not in roulette_winners:
            roulette_winners.append(roulette_winner[0])
    while len(roulette_winners) < 20:
        random_ind_index = random.randint(0,99)
        if individuals[random_ind_index][0] not in roulette_winners:
            roulette_winners.append(individuals[random_ind_index][0])
    return roulette_winners

def get_childs_from_cross_over(individuals):
    childs = []
    while len(childs) < 64:
        random_index_1 = random.randint(0,len(individuals)-1)
        random_index_2 = random.randint(0,len(individuals)-1)
        
        while random_index_1 == random_index_2:
            random_index_1 = random.randint(0,len(individuals)-1)
            random_index_2 = random.randint(0,len(individuals)-1)
        
        individual1 = individuals[random_index_1]
        individual2 = individuals[random_index_2]
        cross_over_childs = cross_over(individual1,individual2)
        if cross_over_childs[0] not in childs:
            childs.append(cross_over_childs[0])
        if cross_over_childs[1] not in childs:
            childs.append(cross_over_childs[1])
    return childs


def build_encryption_key_from_decryption_key(decryption_key):
    encryption_key = []
    for i in range(26):
        encryption_key.append('A')
    for i in range(26):
        encryption_key[ord(decryption_key[i])-65] = chr(i+65)
    return encryption_key

#print (encryption())

def output_decrypt(initial_text, encrypted_text, encryption_rule):
   with open("output.txt", "a") as fd:
       fd.write("Text before encryption is \n{0}\n\n".format(initial_text))
       fd.write("Text after encryption is \n{0}\n\n".format(encrypted_text))
       fd.write("The encryption rule applied is \n{0}\n\n".format(encryption_rule))


def output_generare_indivizi(individuals):
   with open("output.txt", "a") as fd:
       fd.write("\n------Generarea indivizilor:--------\n")
       for individual in individuals:
           fd.write(str(individual))


def output_evaluare_fitness_si_ordonare(ordered_individuals):
   with open("output.txt","a") as fd:
       fd.write("\n-------Afisarea indivizilor sortati dupa valorile de fitness:-----------\n")
       for individual in ordered_individuals:
           fd.write("{0},{1}\n".format(individual[0], individual[1]))


def output_ruleta(ordered_individuals, individuals_from_roulette):
   with open("output.txt", "a") as fd:
       fd.write("\n-------Fitness-ul primului individ------\n")
       fd.write(str(ordered_individuals[0][1]))
       fd.write("\n--------Indivizii din ruleta:---------\n")
       for individ in individuals_from_roulette:
           fd.write(str(individ))

def output_castigatorul_ruletei(individuals, random_individual_index):
   with open("output.txt", "a") as fd:
       fd.write("\n------Castigatorul ruletei este\n{0}\n-----\n".format(individuals[random_individual_index]))


def output_cross_over(individual1, individual2, child1, child2, split_index):
   with open("output.txt", "a") as fd:
       fd.write("\n-----------Cross over----------\n")
       fd.write("Facem split la indexul {0} intre indivizii\n{1}\n si\n{2}\n\n".format(split_index, individual1, individual2))
       fd.write("In urma cross-over-ului au rezultat copiii \n{0}\n si \n{1}\n\n\n".format(child1, child2))




def output_mutation(individual_rezultat, individual, index1, index2):
   with open("output.txt", "a") as fd:
       fd.write("\n---------Procesul de mutatie---------\n")
       fd.write("\n-------Vom aplica mutatia individului \n{0}\n la pozitiile {1} si {2}".format(individual, index1, index2))
       fd.write("\n-------Mutatia rezultata este: \n{0}".format(individual_rezultat))


def output_elite(ordered_individuals):
   with open("output.txt", "a") as fd:
       fd.write("\n-----------Elitismul-------------------\n")
       for i in range(0, 6):
           fd.write(str(ordered_individuals[i])+"\n")

def output_winner_turnir(individual_1, individual_2, scor_1, scor_2):
   with open("output.txt", "a") as fd:
       fd.write("\n-----Lupta turnir intre individul \n{0}\n, avand scorul = {1}, cu individul\n{2}\n, avand scorul = {3}---\n".format(individual_1[0][0], scor_1,individual_2[0][0], scor_2))
       if scor_1 > scor_2:
           fd.write("A castigat individul 1")
       else:
           fd.write("A castigat individul 2")

find_cypher()
