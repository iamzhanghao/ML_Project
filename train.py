import pickle, components, pprint

pp = pprint.PrettyPrinter(indent=5)


def train():
    for language in components.files:

        transition_count = {"start": {}}
        emission_count = {}
        state_count = {}


        # read data
        file = open("raw/" + language + "/train", encoding='utf8')
        rawinput = file.readlines()
        # import data
        data = [{"observation": [], "state": []}]
        index = 0
        for line in rawinput:
            if line == "\n":
                index += 1
                data.append({"observation": [], "state": []})
            else:
                elements = line.split(" ")
                if len(elements) == 2:
                    data[index]['observation'].append(elements[0])
                    data[index]['state'].append(elements[1][:len(elements[1]) - 1])
        data.pop()

        # Count transition
        for line in data:
            ##transition
            for i in range(len(line['state']) + 1):
                if i == 0:
                    ##start

                    from_state = "start"
                    to_state = line['state'][0]
                    if line['state'][0] in transition_count[from_state]:
                        transition_count[from_state][to_state] += 1
                    else:
                        transition_count[from_state][to_state] = 1
                else:
                    ##stop
                    if i == len(line['state']):
                        from_state = line['state'][i - 1]
                        to_state = "stop"
                    ##the rest
                    else:
                        from_state = line['state'][i - 1]
                        to_state = line['state'][i]
                    if from_state in transition_count:
                        if to_state in transition_count[from_state]:
                            transition_count[from_state][to_state] += 1
                        else:
                            transition_count[from_state][to_state] = 1
                    else:
                        transition_count[from_state] = {}
                        transition_count[from_state][to_state] = 1

        # count emission
        for line in data:
            for observation in line['observation']:
                # append empty dict
                emission_count[observation] = {}
                for state in components.states:
                    emission_count[observation][state] = 0

            for observation in line['observation']:
                for state in line['state']:
                    emission_count[observation][state] += 1

        # count state
        for state in components.states:
            state_count[state]=0
        for sentence in data:
            for state in sentence['state']:
                state_count[state] += 1

        # function for a calculation
        def a(f, t, count):
            sum = 0
            for state in count[f]:
                sum += count[f][state]
            return count[f][t] / float(sum)

        # transition parameters
        transition = {}
        for from_state in components.states:
            for to_state in components.states:
                if from_state not in transition:
                    transition[from_state] = {}
                if from_state in transition_count and to_state in transition_count[from_state]:
                    transition[from_state][to_state] = a(from_state, to_state, transition_count)
                else:
                    transition[from_state][to_state] = 0

        # emission parameters
        emission = {}
        for word in emission_count:
            emission[word]={}
            for state in components.states[1:len(components.states)-1]:
                emission[word][state]=emission_count[word][state]/float(state_count[state])

        # for new word
        dev_file = open("raw/" + language + "/dev.in", encoding='utf8')
        dev_lines= dev_file.readlines()
        dev_word_list=[]
        for line in dev_lines:
            if line != "\n":
                dev_word_list.append(line[:len(line)-1])

        for word in dev_word_list:
            if word in emission_count:
                for state in components.states[1:len(components.states)-1]:
                    emission[word][state]=emission_count[word][state]/(float(state_count[state])+1.0)
            else:
                emission[word] = {}
                for state in components.states[1:len(components.states) - 1]:
                    emission[word][state] = 1 / (float(state_count[state]) + 1.0)

        # pp.pprint(emission)

        pickle.dump(transition, open("params/transition/" + language + ".txt", "wb"))
        pickle.dump(emission, open("params/emission/" + language + ".txt", "wb"))

        print("Finished training for " + language)


train()
