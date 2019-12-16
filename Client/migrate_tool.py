# coding: utf-8
from datetime import datetime, timedelta, date
import requests
from dateutil.relativedelta import relativedelta

from kadoudb_access import KadoudbAccess


if __name__ == "__main__":

    api_url = 'https://klnjcc3tc8.execute-api.ap-northeast-1.amazonaws.com/v1/kadou'

    ##
    ## 稼働DBの情報を取得する。
    ##

    # データ抽出期間を設定する。
    firstday = date(2019,1,1)
    today = date(2019,1,31)

    # 稼働DBから稼働情報を取得する
    kadoudb = KadoudbAccess(0)
    res = kadoudb.get_kadou2(firstday, today)
    # print(res)

    # DynamoDBにデータを登録する
    for item in res['data']:
        payload = {}

        try:
            payload['user_account'] = item[1]
            payload['group'] = item[2]
            payload['subgroup'] = item[3]

            start_datetime = datetime(item[4].year, item[4].month, item[4].day, (item[5]-1)//4, ((item[5]-1)%4)*15)
            # 24時の場合は翌日0時に補正
            if item[6] == 97:
                end_datetime = datetime(item[4].year, item[4].month, item[4].day+1, 0, 0)
            else:
                end_datetime = datetime(item[4].year, item[4].month, item[4].day, (item[6]-1)//4, ((item[6]-1)%4)*15)

            payload['start_date'] = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            payload['end_date'] = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            payload['hours'] = item[7]
            payload['wbs_code'] = item[9:15]
            payload['wbs_code_1'] = item[9]
            payload['wbs_code_2'] = '{}-{}'.format(payload['wbs_code_1'], item[10])
            payload['wbs_code_3'] = '{}-{}'.format(payload['wbs_code_2'], item[11])
            payload['wbs_code_4'] = '{}-{}'.format(payload['wbs_code_3'], item[12])
            payload['wbs_code_5'] = '{}-{}'.format(payload['wbs_code_4'], item[13])
            payload['wbs_code_6'] = '{}-{}'.format(payload['wbs_code_5'], item[14])
            payload['comment'] = item[18]
        
        except Error as e:
            print(e)
            continue

        print(payload)

        r = requests.post(api_url params=payload)
        print(r)
