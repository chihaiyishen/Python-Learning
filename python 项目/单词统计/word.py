import io
import re

class Counter:
    def __init__(self, path):
        """
        :param path: 文件路径
        :return:
        """
        # 创建字典变量
        self.mapping = dict()
        # 根据 path 文件路径，创建文件对象 f
        with io.open(path, encoding = 'utf-8') as f:
            # 读取文件数据
            data = f.read()
            # 获取文件里的单词：先转换成小写，在用正则表达式匹配所有的字母。
            words = [s.lower() for s in re.findall("\w+", data)]
            for word in words:
                self.mapping[word] = self.mapping.get(word, 0) + 1

    def most_common(self, n):
        assert n > 0, "n should be large than 0"
        return sorted(self.mapping.items(), key = lambda item: item[1], reverse = True)[:n]

if __name__ == '__main__':
    most_common_5 = Counter("1.txt").most_common(5)
    for item in most_common_5:
        print(item)

