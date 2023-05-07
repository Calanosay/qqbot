import json

pre2 = "C:\\Users\\Administrator\\qqbot\\zzybot\\"


class names:
    def getname(self, people):
        f = open(pre2 + 'name.json', 'r')
        content = f.read()
        a = json.loads(content)
        f.close()
        if people in a:
            return a[people]
        return -1

    def setname(self, people, problem):
        f = open(pre2 + 'name.json', 'r')
        content = f.read()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre2 + "name.json", 'w')
        f2.write(b)
        f2.close()


names = names()
