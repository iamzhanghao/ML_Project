files = ["CN", "EN", "ES", "SG"]
states = ["start", "B-negative", "B-neutral", "B-positive", "O", "I-negative", "I-neutral", "I-positive", "stop"]


class Buffer:
    def __init__(self, size):
        self.__buffer = {}
        for i in range(size):
            self.__buffer[i] = {"p": 0, "previous_state": "NA", "from_k_th": -1}

    def push(self, probablity, previous_state, from_k_th):
        for i in range(self.getSize()):
            if probablity > self.__buffer[i]["p"]:
                for j in range(self.getSize() - 1, i, -1):
                    self.__buffer[j] = self.__buffer[j - 1]
                self.__buffer[i] = {"p": probablity,
                                    "previous_state": previous_state,
                                    "from_k_th": from_k_th}
                break

    def getBuffer(self):
        return self.__buffer

    def getSize(self):
        return len(self.__buffer)

    def getP(self, k):
        return self.__buffer[k]["p"]

    def __str__(self):
        return self.__buffer
