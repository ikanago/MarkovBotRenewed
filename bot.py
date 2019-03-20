import random
import os
from measure_time import measure_time
try:
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
except ImportError:
    pass


class Bot1:
    def __init__(self, corpus, word_length):
        self.corpus = corpus
        self.word_length = word_length

    def utter(self):
        vocab_file = open(self.corpus, "r", encoding="utf-8")
        vocab_list = [vocab for vocab in vocab_file]

        for i in range(10):
            utterance = random.sample(vocab_list, k=self.word_length)
            utterance = [s.strip(os.linesep) for s in utterance]
            utterance = "".join(utterance)
            print(utterance)


class Bot2:
    BEGIN = "__BOS__"
    END = "__EOS__"

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.triplet_list = self.txt2triplet()

    def utter(self):
        """
        n回発話し、ユーザとのインターフェースになる
        """
        # triplet_list = self.triplet_list
        utterance = self.generate_text(self.triplet_list)
        return utterance

    def dialogue(self):
        """
        任意の回数会話を繰り返す
        """
        print("Press enter to have bot speak, or input 'quit' to exit program.")

        triplet_list = self.triplet_list
        while True:
            s = input("Press Enter> ")
            if s == "quit":
                break
            utterance = self.generate_text(triplet_list)
            # エラー処理
            if utterance == "":
                continue
            print(utterance)    # ここは実際にはマイクから発話するメソッドが入る
        # print(os.linesep)

    def generate_text(self, triplet_list):
        """
        ランダムな1文を生成する
        :param triplet_list: 三つ組のlist
        :return: 生成された1文
        """
        utterance = []

        candidate = []
        for s in triplet_list:
            if s[0] == self.BEGIN:
                candidate.append(s)
        first_triplet = random.choice(candidate)
        utterance.append(first_triplet[1])
        utterance.append(first_triplet[2])

        while utterance[-1] != self.END:
            prefix1 = utterance[-2]
            prefix2 = utterance[-1]
            # エラー処理
            try:
                triplet = self.search_triplet(triplet_list, (prefix1, prefix2))
            except IndexError:
                return "error"
            utterance.append(triplet[2])

        result = "".join(utterance[:-1])
        return result

    def txt2triplet(self):
        """
        コーパスの全文を形態素解析して三つ組に分割する
        :return: 三つ組のlist(二次元list)
        """
        triplet_list = []
        with open(self.corpus_path, "r", encoding="utf-8") as corpus:
            for sentence in corpus:
                morphemes = self.morpheme_analysis(sentence)
                triplet = self.generate_triplet(morphemes)
                if len(triplet) != 0:
                    triplet_list.extend(triplet)

        return triplet_list

    @staticmethod
    def morpheme_analysis(sentence):
        """
        1文の形態素解析を行う
        :param sentence: 入力文
        :return: 形態素に分割された文字列型のlist
        """
        token_list = t.tokenize(sentence)
        morphemes = [token.surface for token in token_list]
        return morphemes

    def generate_triplet(self, morphemes):
        """
        形態素に分割された文字列型のlistを三つ組にする
        :param morphemes: 形態素に分割された文字列型のlist
        :return: 三つ組
        """
        if len(morphemes) < 3:
            return []

        triplet = []
        for i in range(len(morphemes) - 2):
            triplet.append(morphemes[i:i+3])

        # BOSを追加
        triplet.insert(0, [self.BEGIN, morphemes[0], morphemes[1]])
        # EOSを追加
        triplet.append([morphemes[-2], morphemes[-1], self.END])

        return triplet

    @staticmethod
    def search_triplet(triplet_list, prefixes):
        """
        三つ組のlistの中から条件(prefixes)に適する三つ組を取得
        :param triplet_list: 三つ組のlist
        :param prefixes: 条件(prefix1, prefix2)
        :return: 三つ組
        """
        candidate = []
        for triplet in triplet_list:
            if triplet[0] == prefixes[0] and triplet[1] == prefixes[1]:
                candidate.append(triplet)

        result = random.choice(candidate)
        return result


class Bot2_neo(Bot2):
    @measure_time
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.triplet_list = self.DB2triplet()

    def utter(self):
        return super().utter()

    def dialogue(self):
        super().dialogue()

    @measure_time
    def DB2triplet(self):
        """
        3-gramで分割されたコーパスを読み込む
        :return: 三つ組のlist(二次元list)
        """
        triplet_list = []

        with open(self.corpus_path, "r", encoding="utf-8") as corpus:
            for triplet in corpus:
                t_list = triplet.strip().split(",")
                triplet_list.append(t_list)

        return triplet_list
