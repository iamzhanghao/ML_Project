files = ["CN", "EN", "ES", "SG"]
states = ["start", "B-negative", "B-neutral", "B-positive", "O", "I-negative", "I-neutral", "I-positive", "stop"]


class Buffer:

    def __init__(self,size):
        self.__buffer={}
        for i in range(size):
            self.__buffer[i]={"p": 0, "path":[]}

    def push(self, item, node):
        for i in range(self.getSize()):
            if item["p"] > self.__buffer[i]["p"]:
                for j in range(self.getSize()-1,i,-1):
                    self.__buffer[j]=self.__buffer[j - 1]
                self.__buffer[i]=item
                self.__buffer[i]["path"].append(node)
                break




    def getBuffer(self):
        return self.__buffer

    def getPath(self,k):
        return self.__buffer[k]["path"]

    def getSize(self):
        return len(self.__buffer)

    def __str__(self):
        return self.__buffer



