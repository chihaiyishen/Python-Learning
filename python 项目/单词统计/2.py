import io
import re

class Koc:
    def __init__(self, path):
        self.mapping = dict()
        with io.open(path, encoding='utf-8') as f:
            data = f.read()
            words = [s.lower() for s in re.findall('\w+', data)]
            for word in words:
                self.mapping[word] = self.mapping.get(word, 0) + 1

    def comm(self):
        return sorted(self.mapping.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    test = Koc('1.txt').comm()
    for i in test:
        print(i)