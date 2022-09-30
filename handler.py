import json
import requests
import datetime
import os
import scmr_housuu
import scmr_jian_jp
import scmr_jian_intl

SLACK_URL = os.environ['SLACK_URL']
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

def main(event, context):
    send_to_slack()
    return {"message": 'send completely'}

def send_to_slack():
    current = datetime.datetime.now().strftime('%Y%m')
    housuu = {'jp': 'housuu_sum_jp_'+current+'.csv', 'intl': 'housuu_sum_intl_'+current+'.csv'}
    jian_jp = {'fn1': 'jian_sum_gen_jp_'+current+'.csv', 'fn2': 'jian_sum_all_jp_'+current+'.csv'}
    jian_intl = {'fn1': 'jian_sum_get_intl_'+current+'.csv', 'fn2': 'jian_sum_all_intl_'+current+'.csv'}
    scmr_housuu.create_csv(housuu)
    scmr_jian_jp.create_csv(jian_jp)
    scmr_jian_intl.create_csv(jian_intl)
    file_path_list = []
    if os.path.isfile('/tmp/'+ housuu['jp']):
        file_path_list.append('/tmp/'+ housuu['jp'])
    if os.path.isfile('/tmp/'+ housuu['intl']):
        file_path_list.append('/tmp/'+ housuu['intl'])
    if os.path.isfile('/tmp/'+ jian_jp['fn1']):
        file_path_list.append('/tmp/'+ jian_jp['fn1'])
    if os.path.isfile('/tmp/'+ jian_jp['fn2']):
        file_path_list.append('/tmp/'+ jian_jp['fn2'])
    if os.path.isfile('/tmp/'+ jian_intl['fn1']):
        file_path_list.append('/tmp/'+ jian_intl['fn1'])
    if os.path.isfile('/tmp/'+ jian_intl['fn2']):
        file_path_list.append('/tmp/'+ jian_intl['fn2'])

    for file_path in file_path_list:
        requests.post(
            url=SLACK_URL,
            params={
                'token': SLACK_TOKEN,
                'channels': SLACK_CHANNEL,
            },
            # まとめて送れない？
            file={'file': (file_path, open(file_path, 'rb'))}
        )
    return
