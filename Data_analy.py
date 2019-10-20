###データ解析モジュール

##現時点ではテキストに次の単語が含まれていたら、単語を返す。
words = ["スポーツ", "アニメ", "ゲーム", "ゲーム", "プログラム"]


def analy(text: str):
    for t in words:
        if t in text:
            return t


import json

import requests as req

import pprint


def wordAnyly(text):
    # header = {"Content-Type": "application/json"}
    #
    # # text = input()
    # param = {"request_id": "record001", "sentence": text, "class_filter": "ART|ORG|PSN|LOC"}
    #
    # APIKEY = "6867436846733131632f4d73646478724e4a566c5679496a325946663957585765716a595a5156526b6236"
    # url = f'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/entity?APIKEY={APIKEY}'
    # r = req.post(url, headers=header, data=json.dumps(param))
    # # pprint.pprint()
    # r=r.json()
    # return [i[0] for i in r["ne_list"]]
    return text.split("、")

# {"word":2}
def countWords(u1:dict)->dict:

    d = {}  # リスト
    for n in u1:
        # print(n)
        for i in u1[n]:
            if i in d:
                # print("true")
                d[i] = d[i] + 1
            else:
                # print("false")
                d[i] = 1

    return max(d.items(), key=lambda x: x[1])

if __name__ =="__main__":
    print(wordAnyly("ラグビーの高橋"))
    # print(countWords({"Usdrksdksd":["ゲーム","スポーツ"],"Usdksdkfsd":["スポーツ","ゲーム","アニメ"],"Usdksdfksd":["ゲーム","スポーツ","読書"]}))