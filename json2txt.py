# -*- coding: utf-8 -*-
import json
import os


def make_vocab_file(input_dir_name, output_file_name):
    """
    jsonファイルが入ったディレクトリを読み込んでテキストファイルを生成する
    :param input_dir_name : 読み込むjsonファイルが入ったディレクトリ名 ※対話破綻コーパスのjsonファイルに限る
    :param output_file_name : 出力するテキストファイル名
    """
    input_dir = os.listdir(input_dir_name)
    output_file = open(output_file_name, "w", encoding="utf-8")

    for file in input_dir:
        path = os.path.join(input_dir_name, file)
        with open(path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            for turn in json_data["turns"]:
                token = turn["utterance"]
                token = modify_str(token)
                output_file.write(token + "\n")

    output_file.close()
    print("Succeeded!")


def modify_str(word):
    """
    入力文字列から特定の文字列を取り除く
    :param word: 入力文字列
    :return: modified_word: 入力から特定の文字列を取り除いた文字列
    """
    # 以下の文字は除外する
    exceptional_char = [',', '.', '、', '。', '?', '？', '!', '！', '「', '」']
    words_list = [c for c in word if c not in exceptional_char]
    modified_word = "".join(words_list)
    return modified_word


if __name__ == '__main__':
    make_vocab_file("JSON_corpus", "vocabulary.txt")
