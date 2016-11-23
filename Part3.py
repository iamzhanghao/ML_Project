import pickle, pprint

pp = pprint.PrettyPrinter(indent=5)

states = ["start", "B-negative", "B-neutral", "B-positive", "O", "I-negative", "I-neutral", "I-positive", "stop"]
# files=["CN","EN","ES","SG"]
files = ["EN"]


transition_dict={}
emission_dict={}

for type in files:

    transition_count = {"start": {}}
    ##read data
    file = open("raw/" + type + "/train", encoding='utf8')
    rawinput = file.readlines()
    ##import data
    data = [[]]
    index = 0
    subindex = 0
    for line in rawinput:
        if line == "\n":
            index += 1
            data.append([])
        else:
            elements = line.split(" ")
            if len(elements) != 0:
                last = elements[len(elements) - 1]
                last = last[:len(last) - 1]
                data[index].append(last)

    data.pop()

    # Count numbers
    for line in data:
        ##transition
        for i in range(len(line) + 1):
            if i == 0:
                ##start
                from_state = "start"
                to_state = line[0]
                if line[0] in transition_count[from_state]:
                    transition_count[from_state][to_state] += 1
                else:
                    transition_count[from_state][to_state] = 1
            else:
                ##stop
                if i == len(line):
                    from_state = line[i - 1]
                    to_state = "stop"
                ##the rest
                else:
                    from_state = line[i - 1]
                    to_state = line[i]
                if from_state in transition_count:
                    if to_state in transition_count[from_state]:
                        transition_count[from_state][to_state] += 1
                    else:
                        transition_count[from_state][to_state] = 1
                else:
                    transition_count[from_state] = {}
                    transition_count[from_state][to_state] = 1

    def a(f, t, count):
        sum = 0
        for state in count[f]:
            sum += count[f][state]
        return count[f][t] / float(sum)

    transition = {}
    for from_state in states:
        for to_state in states:
            if from_state not in transition:
                transition[from_state] = {}
            if from_state in transition_count and to_state in transition_count[from_state]:
                # print("a("+from_state+", "+to_state+") = "+str(a(from_state,to_state)))
                transition[from_state][to_state] = a(from_state, to_state, transition_count)
            else:
                # print("a("+from_state+", "+to_state+") = 0")
                transition[from_state][to_state] = 0

    ####load parameters
    emission = pickle.load(open("emissions/"+type+".txt", "rb"))
    emission_dict[type]=emission
    transition_dict[type]=transition

# pp.pprint(transition_dict)
# pp.pprint(emission_dict)

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
                    p=0
                if p > max_p:
                    max_p = p
                    max_previous_state = previous_state
            path_dict[layer][current_state] = {"p": max_p, "previous": max_previous_state}

    # backtracking
    current_layer = n
    path_reverse = ["stop"]
    while current_layer >= 0:
        path_reverse.append(path_dict[current_layer+1][path_reverse[len(path_reverse)-1]]['previous'])
        current_layer -= 1

    return path_reverse[::-1][1:len(path_reverse)-1]


for type in files:
    # observed_sequence=["Whitney","Houston","fans","to","follow","funeral","on","web","http://t.co/ud9nHNuz"]
    observed_sequence=["is","still","half","clueless","about","twitter","haha"]
    # pp.pprint(emission_dict["EN"])
    pp.pprint(observed_sequence)
    pp.pprint(viterbi(observed_sequence,states,transition_dict[type],emission_dict[type]))




