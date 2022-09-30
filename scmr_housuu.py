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


def substitute(jp_or_intl):
    current = datetime.datetime.now()
    gte = date(current.year, current.month - 1, 1)
    lt = date(current.year, current.month, 1)
    with open("./scmr_housuu.json", "r") as fp:
        dict = json.load(fp)
        for q1 in dict["query"]["bool"]["must"]:
            if "nested" in q1:
                for q2 in q1["nested"]["query"]["bool"]["must"]:
                    if "terms" in q2:
                        q2["terms"]["category.id"] = {"jp": [2], "intl": [3]}[
                            jp_or_intl
                        ]
            if "range" in q1:
                q1["range"]["date_jst"]["gte"] = gte
                q1["range"]["date_jst"]["lt"] = lt
        return json.dumps(dict, indent=2)


def request_opensearch(jp_or_intl):
    data = substitute(jp_or_intl)
    headers = {"content-type": "application/json"}
    res = requests.get(OPENSEARCH_DASHBOARDS + "/_search", data=data, headers=headers)
    return res.text


def create_csv(file_name):
    data = []
    field = ["第一報配信タイトル", "第一報配信日時", "事案番号", "配信数", "URL"]
    data.append(field)

    for key, val in file_name.items():
        source = request_opensearch(key)
        dict = json.loads(source)

        if dict["hits"]["total"]["value"]:
            for bucket in dict["aggregations"]["group_by_jian_no"]["buckets"]:
                tmp = {"title": "", "date": "", "key": "", "num": "", "url": ""}
                tmp["key"] = bucket["key"]
                tmp["url"] = (
                    "https://jp.spectee-dash.com/dashboard/index.php?jian_no="
                    + bucket["key"]
                )
                max = bucket["housuu_list"]["buckets"][0]
                min = bucket["housuu_list"]["buckets"][-1]
                tmp["num"] = max["key"]
                tmp["title"] = min["title"]["buckets"][0]["key"]

                utc_date_str = min["date"]["buckets"][0]["key_as_string"]
                jst_date = datetime.datetime.strptime(
                    utc_date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                ) + datetime.timedelta(hours=-9)
                tmp["date"] = jst_date
                data.append(tmp.values())

            with open("/tmp/" + val, "w", encoding="utf-8") as f:
                write = csv.writer(f)
                write.writerows(data)
if __name__ == "__main__":
    create_csv()
