import pickle, pprint

pp = pprint.PrettyPrinter(indent=5)

CNemission = pickle.load(open("emissions/CNemission.txt", "rb"))
ENemission = pickle.load(open("emissions/ENemission.txt", "rb"))
ESemission = pickle.load(open("emissions/ESemission.txt", "rb"))
SGemission = pickle.load(open("emissions/SGemission.txt", "rb"))
pp.pprint(ESemission)

count_y_y = {"start": {}}
count_y_x = {}

def learn(data):
    for line in data:
        ##transition
        for i in range(len(line[0])+1):
            if i == 0:
                ##start
                from_state = "start"
                to_state = line[0][i]
                if line[0][i] in count_y_y[from_state]:
                    count_y_y[from_state][to_state] += 1
                else:
                    count_y_y[from_state][to_state] = 1
            else:
                ##stop
                if i == len(line[0]):
                    from_state = line[0][i - 1]
                    to_state = "stop"
                ##the rest
                else:
                    from_state = line[0][i -1]
                    to_state = line[0][i]
                if from_state in count_y_y:
                    if to_state in count_y_y[from_state]:
                        count_y_y[from_state][to_state] += 1
                    else:
                        count_y_y[from_state][to_state] = 1
                else:
                    count_y_y[from_state] = {}
                    count_y_y[from_state][to_state] = 1

        for i in range(len(line[0])):
            observation = line[1][i]
            state = line[0][i]
            if state not in count_y_x:
                count_y_x[state] = {}
                count_y_x[state][observation] = 1
            elif observation not in count_y_x[state]:
                count_y_x[state][observation] = 1
            else:
                count_y_x[state][observation] += 1

observed_sequence = ["b","b"]

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
#

