import pprint, pickle, components
from components import *

pp = pprint.PrettyPrinter(indent=5)

transition_dict = {}
emission_dict = {}
observed_sequences_dict = {}
viterbi_dict = {}

top=1


####load parameters
for language in ['EN','ES']:
    emission = pickle.load(open("test/params/emission/" + language + ".txt", "rb"))
    emission_dict[language] = emission

    transition = pickle.load(open("test/params/transition/" + language + ".txt", "rb"))
    transition_dict[language] = transition


def top_k_viterbi(k, observed_sequence, states, a_dict, b_dict):
    pure_state = states[1:len(states) - 1]
    n = len(observed_sequence)

    ###initializing path_dict
    buffer = Buffer(k)
    buffer.push(1.0, "NA", -1)
    path_dict = {0: {"start": buffer}}
    for i in range(n):
        path_dict[i + 1] = {}
    for layer in path_dict:
        if layer == 0: continue
        for state in pure_state:
            path_dict[layer][state] = Buffer(k)
    path_dict[n + 1] = {"stop": Buffer(k)}

    for layer in path_dict:
        if layer == 0: continue

        if layer == n + 1:
            for previous_state in path_dict[layer - 1]:
                for k_th in range(k):
                    p = path_dict[layer - 1][previous_state].getP(k_th) * \
                        a_dict[previous_state]["stop"]
                    path_dict[layer]["stop"].push(p, previous_state, k_th)
            continue

        for current_state in path_dict[layer]:
            for previous_state in path_dict[layer - 1]:
                for k_th in range(k):
                    if current_state in b_dict[observed_sequence[layer - 1]]:
                        p = path_dict[layer - 1][previous_state].getP(k_th) * \
                            a_dict[previous_state][current_state] * \
                            b_dict[observed_sequence[layer - 1]][current_state]
                    else:
                        p = path_dict[layer - 1][previous_state].getP(k_th) * \
                            a_dict[previous_state][current_state] * \
                            0.0000001

                    path_dict[layer][current_state].push(p, previous_state, k_th)

    # # path_dict printing
    # for layer in path_dict:
    #     print("Layer: " + str(layer))
    #     for state in path_dict[layer]:
    #         print("          state: " + state)
    #         for k_th in range(k):
    #             print("                  k_th: " + str(k_th), path_dict[layer][state].getBuffer()[k_th])


    # backtracking
    current_layer = n
    from_k_th = top-1
    path_reverse = ["stop"]
    while current_layer >= 0:
        while path_dict[current_layer + 1][path_reverse[len(path_reverse) - 1]].getBuffer()[from_k_th]['previous_state']== "NA":
            from_k_th-=1
        path_reverse.append(path_dict[current_layer + 1]
                            [path_reverse[len(path_reverse) - 1]].getBuffer()
                            [from_k_th]
                            ['previous_state'])
        from_k_th=path_dict[current_layer + 1][path_reverse[len(path_reverse) - 2]].getBuffer()[from_k_th]['from_k_th']

        current_layer -= 1

    return path_reverse[::-1][1:len(path_reverse) - 1]


#
# language = "EN"
# print(top_k_viterbi(5, ["New", "Year", ",", "New", "Tech", "Writers", "Gathering", "http://nblo.gs/cR1A1"], components.states,
#               transition_dict[language], emission_dict[language]))

for language in ['EN','ES']:
    file = open("test/" + language + "/test.in", encoding='utf8')
    rawinput = file.readlines()

    observed_sequences = [[]]
    index = 0
    for input in rawinput:
        if input == "\n":
            observed_sequences.append([])
            index += 1
        else:
            observed_sequences[index].append(input.strip('\n'))
    observed_sequences.pop()

    states_viterbi = [[]]
    index = 0
    for observed_sequence in observed_sequences:
        for state in top_k_viterbi(top,observed_sequence, components.states, transition_dict[language], emission_dict[language]):
            states_viterbi[index].append(state)
        states_viterbi.append([])
        index += 1
    states_viterbi.pop()

    viterbi_dict[language] = states_viterbi
    observed_sequences_dict[language] = observed_sequences

###write to file
for language in ['EN','ES']:
    msg = ""
    for i in range(len(viterbi_dict[language])):
        for j in range(len(viterbi_dict[language][i])):
            msg += observed_sequences_dict[language][i][j]
            msg += ' '
            msg += viterbi_dict[language][i][j]
            msg += '\n'
        msg += '\n'

    # print(msg)
    result = open("result/" + language + "/test_part4.out", "wb")
    result.write(msg.encode("utf-8"))
    result.close()
    print("test/" + language + "/test.out saved!")

