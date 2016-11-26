import pprint, train_params, pickle, components
from components import *

pp = pprint.PrettyPrinter(indent=5)

transition_dict = {}
emission_dict = {}
observed_sequences_dict = {}

# train_params.train_transition()

####load parameters
for language in components.files:
    emission = pickle.load(open("params/emission/" + language + ".txt", "rb"))
    emission_dict[language] = emission

    transition = pickle.load(open("params/transition/" + language + ".txt", "rb"))
    transition_dict[language] = transition


def top_k_viterbi(k, observed_sequence, states, a_dict, b_dict):
    pure_state = states[1:len(states) - 1]
    n = len(observed_sequence)

    ###initializing path_dict
    buffer = Buffer(k)
    buffer.push({"p": 1.0, "path": []}, "start")
    path_dict = {0: {"start": buffer}}
    for i in range(n):
        path_dict[i + 1] = {}
    for layer in path_dict:
        if layer == 0: continue
        for state in pure_state:
            path_dict[layer][state] = Buffer(k)
    path_dict[n + 1] = {"stop": Buffer(k)}

    pp.pprint(path_dict[0]["start"].getBuffer())

    for layer in path_dict:
        if layer == 0: continue

        if layer == n + 1:
            continue

        for current_state in path_dict[layer]:
            for previous_state in path_dict[layer - 1]:
                for k_th in range(k):
                    if current_state in b_dict[observed_sequence[layer - 1]]:
                        p = path_dict[layer - 1][previous_state].getBuffer()[k_th]["p"] * \
                            a_dict[previous_state][current_state] * \
                            b_dict[observed_sequence[layer - 1]][current_state]
                    else:
                        p = path_dict[layer - 1][previous_state].getBuffer()[k_th]["p"] * \
                            a_dict[previous_state][current_state] * \
                            0.000001
                    print(path_dict[layer-1][previous_state].getPath(k_th))
                    path_dict[layer][current_state].push({'p': p,
                                                          'path': path_dict[layer-1][previous_state].getPath(k_th)},
                                                         current_state)





                    # path_dict[layer][current_state] = {"p": max_p, "previous": max_previous_state}

    #
    # for layer in path_dict:
    #     print("Layer: "+str(layer))
    #     for state in path_dict[layer]:
    #         print("          state: "+state)
    #         print(path_dict[layer][state].getBuffer())
    # pp.pprint(path_dict[0]["start"].getBuffer())


language = "EN"
top_k_viterbi(5, ["New", "Year"], components.states,
              transition_dict[language], emission_dict[language])

#, ",", "New", "Tech", "Writers", "Gathering", "http://nblo.gs/cR1A1"