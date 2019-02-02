from abc import abstractmethod
import numpy as np
import random
import glob
import os
import linecache

from libs.utils import prob, load_chars
from datetime import datetime, timedelta, date


class Corpus(object):
    def __init__(self, chars_file, corpus_dir=None, length=None):
        self.corpus_dir = corpus_dir
        self.length = length
        self.corpus = []

        self.chars_file = chars_file
        self.charsets = load_chars(chars_file)

        if not isinstance(self, RandomCorpus):
            print("Loading corpus from: " + self.corpus_dir)
            self.corpus_path = glob.glob(self.corpus_dir + '/**/*.txt', recursive=True)
            if len(self.corpus_path) == 0:
                print("Corpus not found.")
                exit(-1)

        self.load()

    @abstractmethod
    def load(self):
        """
        Read corpus from disk to memory
        """
        pass

    @abstractmethod
    def get_sample(self):
        """
        Get word line from corpus in memory
        :return: string
        """
        pass


class RandomCorpus(Corpus):
    """
    Load charsets and generate random word line from charsets
    """

    def load(self):
        pass

    def get_sample(self):
        word = ''
        for _ in range(self.length):
            word += random.choice(self.charsets)
        return word


class EngCorpus(Corpus):
    def load(self):
        for i, p in enumerate(self.corpus_path):
            print("Load {}th eng corpus".format(i))
            with open(p, encoding='utf-8') as f:
                data = f.read()

            lines = data.split('\n')
            for line in lines:
                for word in line.split(' '):
                    word = word.strip()
                    word = ''.join(filter(lambda x: x in self.charsets, word))

                    if word != u'' and len(word) > 2:
                        self.corpus.append(word)
            print("Word count {}".format(len(self.corpus)))

    def get_sample(self):
        start = np.random.randint(0, len(self.corpus) - self.length)
        words = self.corpus[start:start + self.length]
        word = ' '.join(words)
        return word


class ChnCorpus(Corpus):
    def load(self):
        """
        Load one corpus file as one line
        """
        for i, p in enumerate(self.corpus_path):
            print_end = '\n' if i == len(self.corpus_path) - 1 else '\r'
            print("Loading chn corpus: {}/{}".format(i + 1, len(self.corpus_path)), end=print_end)
            with open(p, encoding='utf-8') as f:
                data = f.readlines()

            lines = []
            for line in data:
                line_striped = line.strip()
                line_striped = line_striped.replace('\u3000', '')
                line_striped = line_striped.replace('&nbsp', '')
                line_striped = line_striped.replace("\00", "")

                if line_striped != u'' and len(line.strip()) > 1:
                    lines.append(line_striped)

            # 所有行合并成一行
            split_chars = [',', '，', '：', '-', ' ', ';', '。']
            splitchar = random.choice(split_chars)
            whole_line = splitchar.join(lines)

            # 在 crnn/libs/label_converter 中 encode 时还会进行过滤
            whole_line = ''.join(filter(lambda x: x in self.charsets, whole_line))

            if len(whole_line) > self.length:
                self.corpus.append(whole_line)

    def get_sample(self):
        # 每次 gen_word，随机选一个预料文件，随机获得长度为 word_length 的字符
        line = random.choice(self.corpus)

        start = np.random.randint(0, len(line) - self.length)

        word = line[start:start + self.length]
        return word

id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
def gen_id_card(area_code, age, gender):
    datestring = str(date(date.today().year - age, 1, 1) + timedelta(days=random.randint(0, 364))).replace("-", "")
    rd = np.random.randint(0, 999)
    if gender == 0:
        gender_num = rd if rd % 2 == 0 else rd + 1
    else:
        gender_num = rd if rd % 2 == 1 else rd - 1
    result = str(area_code) + datestring + str(gender_num).zfill(3)
    return result + str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])
    
class IdCorpus(Corpus):
    def get_sample(self):
        area_code = np.random.randint(110000, 690000)
        age = np.random.randint(-60, 60)
        gender = np.random.randint(0, 1)
        id_number = gen_id_card(area_code, age, gender)
        return id_number


class NameCorpus(Corpus):
    def load(self):

        family_common_path = os.path.join(self.corpus_dir, "family_common400.txt")
        if not os.path.exists(family_common_path):
            print("family_common400.txt file not exists.")
            exit(1)
        self.family_common = linecache.getlines(family_common_path)

        family_rare_path = os.path.join(self.corpus_dir, "family_rare629.txt")
        if not os.path.exists(family_rare_path):
            print("family_rare629.txt file not exists.")
            exit(1)
        self.family_rare = linecache.getlines(family_rare_path)

        given_common_path = os.path.join(self.corpus_dir, "given_common3980.txt")
        if not os.path.exists(given_common_path):
            print("given_common3980.txt file not exists.")
            exit(1)
        self.given_common = linecache.getlines(given_common_path)

        given_rare_path = os.path.join(self.corpus_dir, "given_rare2537.txt")
        if not os.path.exists(given_rare_path):
            print("given_rare2537.txt file not exists.")
            exit(1)
        self.given_rare = linecache.getlines(given_rare_path)

    def get_sample(self):
        if prob(0.01):
            familyname = random.choice(self.family_rare).strip()
        else:
            familyname = random.choice(self.family_common).strip()
        givenname = ""
        if prob(0.3):
            numchar = 1
        else:
            numchar = 2
        for i in range(0, numchar):
            if prob(0.01):
                givenname += random.choice(self.given_rare).strip()
            else:
                givenname += random.choice(self.given_common).strip()
        name = familyname+givenname
        if len(name)==2:
            name = name[0]+"  "+name[1]
        return name


class SohuCorpus(Corpus):
    def load(self):
        """
        Load one corpus file as one line
        """
        '''
        print(len(self.corpus_path))
        
        for i, p in enumerate(self.corpus_path):
            print_end = '\n' if i == len(self.corpus_path) - 1 else '\r'
            print("Loading chn corpus: {}/{}".format(i + 1, len(self.corpus_path)), end=print_end)
            with open(p, encoding='utf-8') as f:
                data = f.readlines()

            lines = []
            for line in data:
                line_striped = line.strip()
                line_striped = line_striped.replace('\u3000', '')
                line_striped = line_striped.replace('&nbsp', '')
                line_striped = line_striped.replace("\00", "")

                if line_striped != u'' and len(line.strip()) > 1:
                    lines.append(line_striped)

            # 所有行合并成一行
            split_chars = [',', '，', '：', '-', ' ', ';', '。']
            splitchar = random.choice(split_chars)
            whole_line = splitchar.join(lines)

            # 在 crnn/libs/label_converter 中 encode 时还会进行过滤
            whole_line = ''.join(filter(lambda x: x in self.charsets, whole_line))

            if len(whole_line) > self.length:
                self.corpus.append(whole_line)
            '''

    def get_sample(self):
        # 每次 gen_word，随机选一个预料文件，随机获得长度为 word_length 的字符
        filename = random.choice(self.corpus_path)
        with open(filename, encoding='utf-8') as f:
            data = f.readlines()
        whole_line=""
        for line in data:
            line_striped = line.strip()
            line_striped = line_striped.replace('\u3000', '')
            line_striped = line_striped.replace('&nbsp', '')
            line_striped = line_striped.replace("\00", "")
            if line_striped != u'' and len(line.strip()) > 1:
                whole_line += line_striped
        whole_line = ''.join(filter(lambda x: x in self.charsets, whole_line))
        length=self.length-np.random.randint(0,2)
        if len(whole_line) > self.length:
            start = np.random.randint(0, len(whole_line) - length)
            word = line[start:start + length]
        return word