import pickle, pprint, train_params, components

pp = pprint.PrettyPrinter(indent=5)

transition_dict = {}
emission_dict = {}
viterbi_dict = {}
observed_sequences_dict = {}

train_params.train_transition()

####load parameters
for language in components.files:
    emission = pickle.load(open("params/emission/" + language + ".txt", "rb"))
    emission_dict[language] = emission

    transition = pickle.load(open("params/transition/" + language + ".txt", "rb"))
    transition_dict[language] = transition


def viterbi(observed_sequence, states, a_dict, b_dict):
    pure_state = states[1:len(states) - 1]
    n = len(observed_sequence)

    path_dict = {0: {"start": {"p": 1.0, "previous": "NA"}}}

    for i in range(n):
        path_dict[i + 1] = {}
    for layer in path_dict:
        if layer == 0: continue
        for state in pure_state:
            path_dict[layer][state] = {}
    path_dict[n + 1] = {"stop": {}}

    for layer in path_dict:
        if layer == 0: continue

        if layer == n + 1:
            max_p = 0
            max_previous_state = "NA"
            for previous_state in path_dict[layer - 1]:
                p = path_dict[layer - 1][previous_state]["p"] * \
                    a_dict[previous_state]["stop"]
                if p > max_p:
                    max_p = p
                    max_previous_state = previous_state
            path_dict[layer]["stop"] = {"p": max_p, "previous": max_previous_state}
            continue

        for current_state in path_dict[layer]:
            max_p = 0
            max_previous_state = "NA"
            for previous_state in path_dict[layer - 1]:
                if current_state in b_dict[observed_sequence[layer - 1]]:
                    p = path_dict[layer - 1][previous_state]["p"] * \
                        a_dict[previous_state][current_state] * \
                        b_dict[observed_sequence[layer - 1]][current_state]
                else:
                    p = path_dict[layer - 1][previous_state]["p"] * \
                        a_dict[previous_state][current_state] * \
                        0.00001
                if p > max_p:
                    max_p = p
                    max_previous_state = previous_state
            path_dict[layer][current_state] = {"p": max_p, "previous": max_previous_state}

    # backtracking
    current_layer = n
    path_reverse = ["stop"]
    while current_layer >= 0:
        path_reverse.append(path_dict[current_layer + 1][path_reverse[len(path_reverse) - 1]]['previous'])
        current_layer -= 1

    return path_reverse[::-1][1:len(path_reverse) - 1]


for language in components.files:
    file = open("raw/" + language + "/dev.in", encoding='utf8')
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
        for state in viterbi(observed_sequence, components.states, transition_dict[language], emission_dict[language]):
            states_viterbi[index].append(state)
        states_viterbi.append([])
        index += 1
    states_viterbi.pop()

    viterbi_dict[language] = states_viterbi
    observed_sequences_dict[language] = observed_sequences

###write to file
for language in components.files:
    msg = ""
    for i in range(len(viterbi_dict[language])):
        for j in range(len(viterbi_dict[language][i])):
            msg += observed_sequences_dict[language][i][j]
            msg += ' '
            msg += viterbi_dict[language][i][j]
            msg += '\n'
        msg += '\n'

    # print(msg)
    result = open("result/" + language + "/dev.p3.out", "wb")
    result.write(msg.encode("utf-8"))
    result.close()
    print("result/" + language + "/dev.p3.out saved!")

