import random
from janome.tokenizer import Tokenizer
t = Tokenizer()


class DB_txt_constructor:
    BEGIN = "__BOS__"
    END = "__EOS__"

    def __init__(self, corpus_path, output_path):
        self.corpus_path = corpus_path
        self.output_path = output_path

    def output(self):
        triplet_list = self.txt2triplet()
        with open(self.output_path, "w", encoding="utf-8") as db_txt:
            for triplet in triplet_list:
                db_txt.write(triplet + "\n")

    def txt2triplet(self):
        """
        形態素解析されていないコーパスの全文を形態素解析して三つ組に分割する
        :return: tripletをコンマ区切りでまとめたlist
        """
        triplet_list = []
        with open(self.corpus_path, "r", encoding="utf-8") as corpus:
            for sentence in corpus:
                morphemes = self.morpheme_analysis(sentence)
                triplet = self.generate_triplet(morphemes)
                if len(triplet) != 0:
                    triplet_list.extend(triplet)

        joined_triplet_list = ','.join(triplet_list)
        return joined_triplet_list

    @staticmethod
    def morpheme_analysis(sentence):
        """
        ある1文の形態素解析を行う
        :param sentence: 入力文
        :return: 形態素に分割された文字列型のlist
        """
        token_list = t.tokenize(sentence)
        morphemes = [token.surface for token in token_list]
        return morphemes

    def generate_triplet(self, morphemes):
        """
        形態素に分割された文字列型のlistをひとつずつずらしながら三つ組にする
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


class Bot:
    BEGIN = "__BOS__"
    END = "__EOS__"

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.triplet_list = self.DB2triplet()

    def generate_text(self):
        """
        ランダムな1文を生成する
        :param triplet_list: 三つ組のlist
        :return: 生成された1文
        """
        result_list = []

        candidate = []
        for s in self.triplet_list:
            if s[0] == self.BEGIN:
                candidate.append(s)
        first_triplet = random.choice(candidate)
        result_list.append(first_triplet[1])
        result_list.append(first_triplet[2])

        while result_list[-1] != self.END:
            prefix1 = result_list[-2]
            prefix2 = result_list[-1]
            # エラー処理
            try:
                triplet = self.search_triplet(self.triplet_list, (prefix1, prefix2))
            except IndexError:
                return "error"
            result_list.append(triplet[2])

        result = "".join(result_list[:-1])
        return result

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
