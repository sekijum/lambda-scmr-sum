#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import json
import csv
import io, sys
import requests
import datetime
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
OPENSEARCH_DASHBOARDS = os.environ["OPENSEARCH_DASHBOARDS"]


def date(year, mounth, day):
    return datetime.datetime(
        year, mounth, day, tzinfo=datetime.timezone(datetime.timedelta(hours=9), "JST")
    ).isoformat()


def substitute():
    current = datetime.datetime.now()
    gte = date(current.year, current.month - 1, 1)
    lt = date(current.year, current.month, 1)
    with open("./scmr_jian_jp.json", "r") as fp:
        dict = json.load(fp)
        for q1 in dict["query"]["bool"]["must"]:
            if "range" in q1:
                q1["range"]["date_jst"]["gte"] = gte
                q1["range"]["date_jst"]["lt"] = lt
        return json.dumps(dict, indent=2)


def request_opensearch():
    data = substitute()
    headers = {"content-type": "application/json"}
    res = requests.get(OPENSEARCH_DASHBOARDS + "/_search", data=data, headers=headers)
    return res.text
    # try:
    #     print('try')
    #     with urllib.request.urlopen(url) as res:
    #         print("======")
    #         print(res)
    #         body = res
    #         #print('body')
    #         jl= json.load(body)
    #         exit
    #         return jl
    # except urllib.error.HTTPError as err:
    #     print(err.code)
    # except urllib.error.URLError as err:
    #     print(err.reason)
    # exit


# 結果のJSONをロードする


# CSVの見出し行と列を定義する


# ロードしたオブジェクトをループで回す

# jf = open("cases_request202108.json", "r")
# jl = json.load(jf)

# print(jl["aggregations"]["nexted_by_geo"]["group_by_geo_city"]["buckets"][0]["reverse"]["nested_by_tag"]["group_by_tag"]["buckets"][0]["doc_count"])


# def set_csvfile():


def create_csv(file_name):
    jl = request_opensearch()
    # pprint.pprint(jl)
    prefs = [
        "北海道","青森県","岩手県","秋田県","宮城県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"
    ]

    # tags = [
    #     100100001,100100110,100100120,100100130,100100140,100100150,100100160,100100170,100100210,100100220,100100311,100100310,100100320,100100330,100100410,100100420,100100440,100100430,100100510,100100520,100100530,100100540,100100610,100100620,100100710,100100720,100100730,100100740,100100750,100100810,100100820,100100910,100100920,100100930,100101000,100200001,100200010,100200020,100200030,100200040,100200050,100200060,100300001,100300002,100300003,100300004,100300005,100300008,100300009,100300010,100300011,100400001,100400002,100400003,100400004,100400022,100400005,100400006,100400007,100400008,100400009,100400010,100400011,100400012,100400013,100400014,100400015,100400016,100400017,100400018,100400019,100400020,100400021,100500001,100500002,100500003,100500004,100500005,100500006,100500007,100500008,100500009,100500010,100600001,100600002,100600003,100600004,100600005,100600006,100600007,100600008,100500011,200100001,200100002,200100003,200100004,200100005,200100006,200100007,200100008,200100009,200100010,200100011,200100012,200100013,200100014,200100015,200100016,800300001,800300002,800300003,900100001,900100002,900100003,900100004,900100005,900100006,900100007,900100008,900100009,900100010,900100011,900100012,900100013,900100014,900100015,900100016,900100017,900100018,900100019,900100020,900100021,900100022,900100023,900100024,900100025,900100026,900100027,900100028,900100029,900100030,900100031,900100032,900100033,900100034,900100035,900100036,900100037,900100038,900100039,900100040,900100041,900100042,900100043,900100044,900100045,900100046,900100047,900100098,900100099,900101001,900101002,900101003,900101004,900101005,900101006,900101007,900101008,900101009,900101010,900101011,900101012,900101013,900101014,900101015,900101016,900101017,900101018,900101019,900101020,900101021,900101022,900101023,900101024,900101025,900101026,900101027,900101028,900101029,900101030,900101031,900101032,900101033,900101034,900101035,900101036,900101037,900101999
    # ]
    tagnames1 = [
        "気象災害全般","火災全般","事故全般","事件全般","生活基盤全般","その他全般"
    ]
    tagnames2 = [
        "自動車","鉄道","新幹線","飛行機・ヘリ","船舶","山林","駅","主要駅","沿線・路線","空港","高速道路","ビル・商業施設","工場・倉庫","発電所","河川","国道","気象・災害","気象災害全般","落雷","大雨","大雨被害","雨漏り","土砂災害","氾濫・洪水","浸水・冠水","崩落・倒壊","倒木","降雪","雪被害","雪崩","降雹","竜巻・つむじ風","強風・暴風","台風","台風被害","地震","地震被害","液状化","津波","噴火","降灰","濃霧","大気現象","自然現象","天文現象","季節現象","熱中症","花粉","高波・高潮","救助要請","避難情報","気象災害情報","火災全般","火事","爆発","発煙","報知器作動","消防出動","大規模火災","事故全般","炎上事故","横転事故","危険走行","落下物","故障","人身事故","居眠り","水難事故","事件全般","不審者","立てこもり","誘拐","盗難・窃盗","強盗","発砲","破損","異臭","危険物","不審物","不発弾","自殺","犯行予告","殺人","死体遺棄・発見","テロ","デモ","暴力行為","軍事・クーデター","警察出動","救急出動","生活基盤全般","停電","電力設備トラブル","ガス漏れ","断水・濁水","水道管破裂","道路異常","ガス爆発","システム・通信障害","渋滞・混雑","遅延・運休・停止","その他全般","不祥事","異物混入","動物出没","スポーツ・イベント","感染症","デマ情報","密集"
    ]


    with open("/tmp/" + file_name['fn1'], "w", encoding="utf-8") as fp1:
        with open("/tmp/" + file_name['fn2'], "w", encoding="utf-8") as fp2:

            cw1 = csv.writer(fp1)
            cw2 = csv.writer(fp2)

            # 見出し行の作成
            title1 = [""] + tagnames1
            title2 = [""] + tagnames2
            cw1.writerow(title1)
            cw2.writerow(title2)
            cols = []
            for pref in prefs:
                cols.append(pref)
            # cw.writerows(cols)
            jl2 = json.loads(jl)
            for b1 in jl2["aggregations"]["nexted_by_geo"]["group_by_geo_city"]["buckets"]:
                # print(b1)
                if not b1["key"] in prefs:
                    continue
                row1 = []
                row2 = []
                row1.append(b1["key"])
                row2.append(b1["key"])
                for tag in tagnames1:
                    count = 0
                    for b2 in b1["reverse"]["nested_by_tag"]["group_by_tag"]["buckets"]:
                        if b2["key"] == str(tag):
                            count = int(b2["doc_count"])
                            break
                    row1.append(count)
                cw1.writerow(row1)
                for tag in tagnames2:
                    count = 0
                    for b2 in b1["reverse"]["nested_by_tag"]["group_by_tag"]["buckets"]:
                        if b2["key"] == str(tag):
                            count = int(b2["doc_count"])
                            break
                    row2.append(count)
                cw2.writerow(row2)
if __name__ == "__main__":
    create_csv()
