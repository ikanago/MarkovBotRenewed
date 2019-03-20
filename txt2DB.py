from bot import Bot2


def make_DB_file(input_file_name, output_file_name):
    """
    テキストファイルから一行ずつ読み込んで、3-gram に分割して出力ファイルに書き込む
    :param input_file_name: 読み込むコーパス
    :param output_file_name: 出力ファイル
    """
    bot = Bot2(input_file_name)

    triplet_list = bot.txt2triplet()

    with open(output_file_name, "w", encoding="utf-8") as f_out:
        for triplet in triplet_list:
            f_out.write(",".join(triplet) + "\n")

    print("Succeeded!")


if __name__ == '__main__':
    make_DB_file("output.txt", "output_DB(1).csv")
