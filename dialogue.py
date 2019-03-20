from bot import Bot2_neo
import socket
import subprocess
import xml.etree.ElementTree as ET


# あらかじめ call_jtalk.sh に実行権限を与えておく
def jtalk(t):
    subprocess.call(["echo call_jtalk.sh" + t], shell=True)


if __name__ == '__main__':
    bot = Bot2_neo("vocabulary_DB.txt")

    HOST = "<address>"
    PORT = 0    # ポート番号

    p = subprocess.Popen(["bash exec_julius.sh"], stdout=subprocess.PIPE, shell=True)
    pid = p.stdout.read()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    try:
        data = ""
        while True:
            if "<RECOGOUT>\n" in data:
                root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n", ""))
                for whypo in root.findall('./SHYPO/WHYPO'):
                    call = whypo.get("WORD")
                    if call == "ラピロ":
                        jtalk(bot.utter(1))
                        data = ""
                    elif call == "終わり":
                        break

            else:
                data += client.recv(1024)

    except KeyboardInterrupt:
        client.close()
        print("Keyboard interrupt occur.")
        p.kill()
        subprocess.call(["kill " + pid], shell=True)
        client.close()
