import pickle


files=["CN","EN","ES","SG"]

for language in files:
    file = open("raw/" + language + "/train", encoding='utf8')
    en_file = file.readlines()
    y = {}
    for i in en_file:
        i = i.replace("\n", "")
        array = i.split(" ")
        if len(array) == 2:
            if array[1] not in y.keys():
                y[str(array[1])] = 0
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

    pickle.dump(emission, open("emissions/" + language + ".txt", "wb"))


for language in files:

    emission = pickle.load(open("emissions/" + language + ".txt", "rb"))
    testfile = open("raw/"+language+"/dev.in", encoding='utf8')
    test_x = testfile.readlines()
    result = open("result/"+language+"/dev.p2.out", "wb")
    x = {}

    for i in test_x:
        i = i.replace("\n", "")
        if i != "":
            score = 0.0
            temp = ""
            for j in emission[i].keys():
                if emission[i][j] >= score:
                    score = emission[i][j]
                    temp = j
            line = i + " " + temp + "\n"
            result.write(line.encode("utf-8"))
        else:
            result.write("\n".encode("utf-8"))

    result.close()

