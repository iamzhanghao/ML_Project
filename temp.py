emission = pickle.load(open("D:\Study\Term 6\Machine learning\CN\\emission2.txt", "rb"))
testfile = open("D:\Study\Term 6\Machine learning\CN\\dev.in", encoding='utf8')
test_x = testfile.readlines()
result=open("D:\Study\Term 6\Machine learning\CN\\dev.prediction", "wb")
x = {}

for i in test_x:
    i = i.replace("\n", "")
    if i != "":
        score = 0.0
        temp = ""
        for j in emission[i].keys():
            if emission[i][j]>=score:
                score=emission[i][j]
                temp=j
        line=i+" "+temp+"\n"
        result.write(line.encode("utf-8"))
    else:
        result.write("\n".encode("utf-8"))