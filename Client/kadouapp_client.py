# coding: utf-8
from datetime import datetime, timedelta, date
import sys
from pprint import pprint
from dateutil.relativedelta import relativedelta

from kadoudb_access import KadoudbAccess
from outlook_access import OutlookScheduleAccess


if __name__ == "__main__":

    ##
    ## Outlookから予定を取得する。
    ##

    # outlookスケジュールのオブジェクトを取得する。
    outlook = OutlookScheduleAccess()
    print(outlook.name)
    
    # プログラム実行日の月初から当日の予定を取得する。
    today = date.today()
    firstday = date.today().replace(day=1)
    schedule_list = outlook.get_schedule(from_date=firstday, to_date=today)

    # 予定の重複を排除する。
    deduplicated_schedule = outlook.deduplicate_schedule(schedule_list)

    # debug
    print(today)
    print(firstday)
    print('schedule list : ')
    pprint(schedule_list)
    print()
    print('deduplicated schedule list : ')
    pprint(deduplicated_schedule)
    print()


    ##
    ## 稼働DBの情報を取得する。
    ##

    # 稼働DBからユーザ情報を取得する。
    kadoudb_pp = KadoudbAccess(0)
    userdata_pp = kadoudb_pp.get_user(outlook.name)
    kadoudb_bp = KadoudbAccess(1)
    userdata_bp = kadoudb_bp.get_user(outlook.name)
    
    # ユーザ情報から稼働サーバを識別する。
    if userdata_pp['data'] is not None:
        kadoudb = kadoudb_pp
        userdata = userdata_pp
    elif userdata_bp['data'] is not None:
        kadoudb = kadoudb_bp
        userdata = userdata_bp
    else:
        print('稼働DBにユーザがありません')
        sys.exit()
    
    # debug
    print(userdata)


    ##
    ## 稼働DBに情報を登録する。
    ##

    # 稼働DBから指定期間の稼働データを削除する。
    res = kadoudb.delete_kadou(userdata['data'], firstday, today)

    # debug
    print(res)

    # 稼働DBに稼働データを登録する。
    for schedule in deduplicated_schedule:
        kadoudb.post_kadou(userdata['data'], schedule)
