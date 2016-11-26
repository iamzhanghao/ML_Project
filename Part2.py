import pickle
import train_params, components

train_params.train_emission()

for language in components.files:

    emission = pickle.load(open("params/emission/" + language + ".txt", "rb"))
    testfile = open("raw/" + language + "/dev.in", encoding='utf8')
    test_x = testfile.readlines()
    result = open("result/" + language + "/dev.p2.out", "wb")
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
