import pickle, pprint

pp = pprint.PrettyPrinter(indent=5)
# files=["CN","EN","ES","SG"]
files = ["CN"]

CNemission = pickle.load(open("emissions/CN.txt", "rb"))
ENemission = pickle.load(open("emissions/EN.txt", "rb"))

transition_count = {"start": {}}

for type in files:
    file = open("raw/" + type + "/train", encoding='utf8')
    rawinput = file.readlines()
    # pp.pprint(rawinput)

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

    # pp.pprint(transition_count)

states = ["start", "B-negative", "B-neutral", "B-positive","O", "I-negative", "I-neutral", "I-positive", "stop"]
transition = {}


def a(f, t, count):
    sum = 0
    for state in count[f]:
        sum += count[f][state]
    return count[f][t] / float(sum)


for from_state in states:
    for to_state in states:
        print(from_state)
        print(to_state)
        if from_state not in transition:
            transition[from_state] = {}
        if from_state in transition_count and to_state in transition_count[from_state]:
            # print("a("+from_state+", "+to_state+") = "+str(a(from_state,to_state)))
            transition[from_state][to_state] = a(from_state, to_state, transition_count)
        else:
            # print("a("+from_state+", "+to_state+") = 0")
            transition[from_state][to_state] = 0
# pp.pprint(transition)









#
# observed_sequence = ["b","b"]
#
# def viterbi(observed_sequence,states):
#     pure_state=states[1:len(states)-1]
#     path=["start"]
#     n=len(observed_sequence)
#
#     path_dict={0:{"start":{"p":1.0,"previous":"NA"}}}
#
#     for i in range(n):
#         path_dict[i+1]={}
#     for layer in path_dict:
#         if layer==0: continue
#         for state in pure_state:
#             path_dict[layer][state]={}
#     path_dict[n+1]={"stop":{}}
#
#     for layer in path_dict:
#         if layer==0 : continue
#
#         if layer==n+1:
#             max_p = 0
#             max_previous_state = "NA"
#             for previous_state in path_dict[layer - 1]:
#                 p = path_dict[layer - 1][previous_state]["p"] * \
#                     a_dict[previous_state]["stop"]
#                 if p > max_p:
#                     max_p = p;
#                     max_previous_state = previous_state
#             path_dict[layer]["stop"] = {"p": max_p, "previous": max_previous_state}
#             continue
#
#         for current_state in path_dict[layer]:
#             max_p = 0
#             max_previous_state = "NA"
#             for previous_state in path_dict[layer-1]:
#                 p=path_dict[layer-1][previous_state]["p"]*\
#                   a_dict[previous_state][current_state]*\
#                   b_dict[current_state][observed_sequence[layer-1]]
#                 if p>max_p:
#                     max_p=p;
#                     max_previous_state=previous_state
#             path_dict[layer][current_state]={"p":max_p,"previous":max_previous_state}
#
