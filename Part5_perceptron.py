import pprint
from components import Buffer

pp = pprint.PrettyPrinter(indent=5)

states = ["NULL", "B-negative", "O", "B-neutral", "B-positive", "I-negative", "I-neutral", "I-positive"]

ITER = 70

TOP_train = 1

TOP_predict = 1

CLEAN_DATA = True

print("ITER", ITER)
print("TOP_train", TOP_train)
print("TOP_predict", TOP_predict)


def viterbi(k, transition, emission, words):
    # print("Veterbi")
    # print(words)

    n = len(words)

    path_dict = {}

    for i in range(n):
        path_dict[i] = {}
    for layer in path_dict:
        for state in states[1:]:
            path_dict[layer][state] = Buffer(k)

    path_dict[n] = {'stop': Buffer(k)}

    for layer in path_dict:

        if layer == n:
            for previous_state in states[1:]:
                for k_th in range(k):
                    p = path_dict[layer - 1][previous_state].getP(k_th) + \
                        transition[previous_state][current_state]['NULL']
                    path_dict[layer]['stop'].push(p, previous_state, k_th)
            continue

        if layer == 1:
            for previous_state in states[1:]:
                for current_state in states[1:]:
                    for k_th in range(k):
                        p = path_dict[layer - 1][previous_state].getP(k_th) + \
                            transition['NULL'][previous_state][current_state] + \
                            emission[words[layer]][current_state]
                        path_dict[layer][current_state].push(p, previous_state, k_th)
            continue

        if layer == 0:
            for current_state in states[1:]:
                for k_th in range(k):
                    p = transition['NULL']['NULL'][current_state] + \
                        emission[words[layer]][current_state]
                    path_dict[layer][current_state].push(p, "NA", k_th)
            continue

        for previous_state in states[1:]:
            for current_state in states[1:]:
                for k_th in range(k):
                    p = path_dict[layer - 1][previous_state].getP(k_th) + \
                        transition[path_dict[layer - 1][previous_state].getPrevious(k_th)][previous_state][
                            current_state] + \
                        emission[words[layer]][current_state]
                    path_dict[layer][current_state].push(p, previous_state, k_th)

    # # path_dict printing
    # for layer in path_dict:
    #     print("Layer: " + str(layer))
    #     for state in path_dict[layer]:
    #         print("          state: " + state)
    #         for k_th in range(k):
    #             print("                  k_th: " + str(k_th), path_dict[layer][state].getBuffer()[k_th])
    #
    #
    top = 1
    current_layer = n - 1
    from_k_th = top - 1
    path_reverse = ["stop"]
    while current_layer >= 0:
        while path_dict[current_layer + 1][path_reverse[len(path_reverse) - 1]].getBuffer()[from_k_th][
            'previous_state'] == "NA":
            from_k_th -= 1
        path_reverse.append(path_dict[current_layer + 1]
                            [path_reverse[len(path_reverse) - 1]].getBuffer()
                            [from_k_th]
                            ['previous_state'])
        from_k_th = path_dict[current_layer + 1][path_reverse[len(path_reverse) - 2]].getBuffer()[from_k_th][
            'from_k_th']

        current_layer -= 1

    return path_reverse[::-1][:len(path_reverse) - 1]


def perceptron(tag_predictions, tags, words, transition, emission):
    n = len(tags)
    for i in range(n):
        emission[words[i]][tags[i]] += 1
        emission[words[i]][tag_predictions[i]] -= 1
        if i == 0:
            transition["NULL"]["NULL"][tags[0]] += 1
            transition["NULL"]["NULL"][tag_predictions[0]] -= 1
        elif i == 1:
            transition["NULL"][tags[0]][tags[1]] += 1
            transition["NULL"][tag_predictions[0]][tag_predictions[1]] -= 1
        else:
            transition[tags[i - 2]][tags[i - 1]][tags[i]] += 1
            transition[tag_predictions[i - 2]][tag_predictions[i - 1]][tag_predictions[i]] -= 1

    return transition, emission


def clean(word):
    if CLEAN_DATA:
        word = word.replace("\n",'')
        return word.lower()
    else:
        return word


print("Computing....")

for language in ['EN']:
    print(language)
    train_file = open("raw/" + language + "/train", encoding='utf8')
    test_file = open("raw/" + language + "/dev.in", encoding='utf8')

    transition = {}
    for state in states:
        transition[state] = {}
        for state_2 in states:
            transition[state][state_2] = {}
            for state_3 in states:
                transition[state][state_2][state_3] = 0

    lines = train_file.readlines()

    emission = {}
    for line in lines:
        if line != "\n":
            word = line.split(" ")[0]
            if word not in emission.keys():
                emission[clean(word)] = {}
                for state in states[1:]:
                    emission[clean(word)][state] = 0

    train_tag_data = [[]]
    train_word_data = [[]]
    cleaned_train_word_data=[[]]
    index = 0
    for line in lines:
        if line == '\n':
            index += 1
            train_tag_data.append([])
            train_word_data.append([])
            cleaned_train_word_data.append([])
            continue
        word = line.split(' ')[0]
        tag = line.split(' ')[1]
        train_tag_data[index].append(tag[:-1])
        train_word_data[index].append(word)
        cleaned_train_word_data[index].append(clean(word))

    train_tag_data.pop()
    train_word_data.pop()
    cleaned_train_word_data.pop()

    # add new word
    lines = test_file.readlines()
    for line in lines:
        if line != "\n":
            word = line[:-1]
            if word not in emission.keys():
                emission[clean(word)] = {}
                for state in states[1:]:
                    emission[clean(word)][state] = 0

    test_word_data = [[]]
    cleaned_test_word_data = [[]]
    index = 0
    for line in lines:
        if line == '\n':
            index += 1
            test_word_data.append([])
            cleaned_test_word_data.append([])
            continue
        word = line[:-1]
        test_word_data[index].append(word)
        cleaned_test_word_data[index].append(clean(word))

    test_word_data.pop()
    cleaned_test_word_data.pop()



    ##train
    for i in range(ITER):
        for j in range(len(train_tag_data)):
            prediction = viterbi(TOP_train, transition, emission, cleaned_train_word_data[j])
            transition, emission = perceptron(prediction, train_tag_data[j], cleaned_train_word_data[j], transition, emission)

    msg = ''
    for i in range(len(test_word_data)):
        prediction = viterbi(TOP_predict, transition, emission, cleaned_test_word_data[i])
        for j in range(len(test_word_data[i])):
            msg += test_word_data[i][j]
            msg += ' '
            msg += prediction[j]
            msg += '\n'
        msg += '\n'

    result = open("result/" + language + "/dev.p5.out", "wb")
    result.write(msg.encode("utf-8"))
    result.close()

    pp.pprint(emission)
    pp.pprint(transition)
    print(language)

print("Done")

print("ITER", ITER)
print("TOP_train", TOP_train)
print("TOP_predict", TOP_predict)
