import pickle, components, pprint

pp = pprint.PrettyPrinter(indent=5)


def train_emission():
    for language in components.files:
        file = open("raw/" + language + "/train", encoding='utf8')
        en_file = file.readlines()
        y = {}
        for i in en_file:
            i = i.replace("\n", "")
            array = i.split(" ")
            if len(array) == 2:
                if array[1] not in y.keys():
                    y[str(array[1])] = 0##################################################0
                else:
                    y[str(array[1])] += 1
        testfile = open("raw/" + language + "/dev.in", encoding='utf8')
        test_x = testfile.readlines()
        x = []
        counter = 0
        for i in test_x:
            counter += 1
            i = i.replace("\n", "")
            if i != "" and i not in x:
                x.append(i)

        emission = {}
        for i in en_file:
            i = i.replace("\n", "")
            array = i.split(" ")
            if len(array) == 2:
                if str(array[0]) not in emission.keys():
                    emission[str(array[0])] = {array[1]: 1}

                elif str(array[1]) not in emission[str(array[0])].keys():
                    emission[str(array[0])][array[1]] = 1

                else:
                    emission[str(array[0])][array[1]] += 1

        for i in emission.keys():
            if i in x:
                for k in emission[i].keys():
                    emission[i][k] = emission[i][k] * 1.0 / (y[k] + 1)
            else:
                for k in emission[i].keys():
                    emission[i][k] = emission[i][k] * 1.0 / y[k]

        for i in x:
            if i not in emission.keys():
                emission[str(i)] = {}
                for j in y.keys():
                    emission[str(i)][j] = 1.0 / (y[j] + 1)
        #
        # for word in emission:
        #     for state in y.keys():
        #         if state not in emission[word]:
        #             emission[word][state]=0.0

        pp.pprint(y)

        pickle.dump(emission, open("params/emission/" + language + ".txt", "wb"))
        print("Finished training emission params for "+ language)



def train_transition():

    for language in components.files:

        transition_count = {"start": {}}
        ##read data
        file = open("raw/" + language + "/train", encoding='utf8')
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
        for from_state in components.states:
            for to_state in components.states:
                if from_state not in transition:
                    transition[from_state] = {}
                if from_state in transition_count and to_state in transition_count[from_state]:
                    transition[from_state][to_state] = a(from_state, to_state, transition_count)
                else:
                    transition[from_state][to_state] = 0

        pickle.dump(transition, open("params/transition/" + language + ".txt", "wb"))
        print("Finished training transition params for "+ language)

#
train_emission()
train_transition()
