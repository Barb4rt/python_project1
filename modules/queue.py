from threading import Thread


class ThreadHandler(Thread):
    def __init__(self, threadID, name, target):
        Thread.__init__(self, target=target)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        print("Exiting " + self.name)
