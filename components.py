class Buffer:

    def __init__(self, size):
        self.buffer={}
        for i in range(size):
            self.buffer[i]={"p": 0, "path":{}}

    def push(self, item, node):
        for i in range(self.getSize()):
            continue


    def getSize(self):
        return len(self.buffer)