# coding: utf-8
import mysql.connector
from datetime import datetime, timedelta, date


class KadoudbAccess:

    DB_CONFIG = ({
        'user': 'kanri',
        'password': 'kanri', 
        'host': 'sh2kadou', 
        'database': 'sh2kadou1', 
        'charset': 'sjis'
        },
        {
        'user': 'kanri',
        'password': 'kanri', 
        'host': 'sh2kadou', 
        'database': 'sh2kadou2', 
        'charset': 'sjis'
        })


    '''
    コンストラクタ
    DBサーバの種別（0:proper、1:partner）、DBの接続情報を設定する。
    '''
    def __init__(self, server_id=0):
        if server_id != 0:
            server_id = 1 

        self.server_id = server_id
        self.config = Kadoudb.DB_CONFIG[server_id]


    '''
    氏名（姓 名）をキーに稼働DBからユーザ情報（会社ID, アカウント, グループID, サブグループID）をタプル形式で取得する。
    '''
    def get_user(self, username):

        #SQL定義
        sql = '\
            SELECT DISTINCT\
                CORPID,\
                ACCOUNT,\
                G,\
                SG\
            FROM\
                TBL_USER\
            WHERE\
                NAME = %s\
            '

        # 稼働DBに接続
        res = {}
        try:
            connector = mysql.connector.connect(**self.config)

            # SQL実行
            cursor = connector.cursor()
            cursor.execute(sql, (username, ))
            res = { 'data': cursor.fetchone() }

        except mysql.connector.Error as e:
            print("Error:", e)
            print("Error:", str(e))
            res = { 'error': 'db connection error' }

        finally:
            # データベースから切断
            cursor.close()
            connector.close()

        return res


    '''
    ユーザ情報と予定情報もとに稼働情報を登録する。
    入力値：
        userdata：(会社ID, アカウント, グループID, サブグループID）
        schedule：{"start": , "end": , "wbscode": , "comment": , "date": , "delta", }
    '''
    def post_kadou(self, userdata, schedule):

        #SQL定義
        sql = '\
            INSERT INTO TBL_KADOU\
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\
            '

        stimeid = schedule['start'].hour * 4 + round(schedule['start'].minute / 15) + 1
        etimeid = schedule['end'].hour * 4 + round(schedule['end'].minute / 15) + 1
        time = (etimeid - stimeid) * 0.25

        post_data = (
            userdata[0], #CORPID
            userdata[1], #ACCOUNT
            userdata[2], #G
            userdata[3], #SG
            schedule['start'].strftime('%Y/%m/%d'), #DATE
            stimeid, #STIMEID
            etimeid, #ETIMEID
            time, #TIME
            1, #SEIDOID
            schedule['wbscode'][0], #GYOUMUID
            schedule['wbscode'][1], #EVENTID
            schedule['wbscode'][2], #LCATEGORY
            schedule['wbscode'][3], #MCATEGORY
            schedule['wbscode'][4], #SCATEGORY
            schedule['wbscode'][5], #VSCATEGORY
            0, #PRODUCTID
            0, #PRODUCTAMOUNT
            None, #RENRAKUHYOUID
            schedule['comment'] #COMMENT
            )
        
        print(post_data)

        # 稼働DB
        res = { 'data': post_data }
        try:
            connector = mysql.connector.connect(**self.config)
            # SQL実行
            cursor = connector.cursor()
            cursor.execute(sql, post_data)
            connector.commit()
            
        except mysql.connector.Error as e:
            print("Error:", e)
            print("Error:", str(e))
            res = { 'error': 'db connection error' }

        finally:           
            # データベースから切断
            cursor.close()
            connector.close()

        return res


    '''
    指定されたユーザ、期間の稼働情報を取得する。
    入力値：
        userdata：(会社ID, アカウント, グループID, サブグループID）
        from_date：datetime.date
        to_date：datetime.date
    '''
    def get_kadou(self, userdata, from_date=date.today(), to_date=date.today()):

        #SQL定義
        sql = '\
            SELECT * FROM TBL_KADOU\
            WHERE\
                ACCOUNT = %s AND\
                DATE BETWEEN %s AND %s\
            '
        res = {}
        try:
            connector = mysql.connector.connect(**self.config)

            # SQL実行
            cursor = connector.cursor()
            cursor.execute(sql, (userdata[1], from_date.strftime('%Y/%m/%d'), to_date.strftime('%Y/%m/%d')))
            res = { 'data': cursor.fetchall() }

        except mysql.connector.Error as e:
            print("Error:", e)
            print("Error:", str(e))
            res = { 'error': 'db connection error' }

        finally:
            # データベースから切断
            cursor.close()
            connector.close()

        return res

    '''
    指定されたユーザ、期間の稼働情報を取得する。
    入力値：
        userdata：(会社ID, アカウント, グループID, サブグループID）
        from_date：datetime.date
        to_date：datetime.date
    '''
    def get_kadou2(self, from_date=date.today(), to_date=date.today()):

        #SQL定義
        sql = '\
            SELECT * FROM TBL_KADOU\
            WHERE\
                DATE BETWEEN %s AND %s\
            '
        res = {}
        try:
            connector = mysql.connector.connect(**self.config)

            # SQL実行
            cursor = connector.cursor()
            cursor.execute(sql, (from_date.strftime('%Y/%m/%d'), to_date.strftime('%Y/%m/%d')))
            res = { 'data': cursor.fetchall() }

        except mysql.connector.Error as e:
            print("Error:", e)
            print("Error:", str(e))
            res = { 'error': 'db connection error' }

        finally:
            # データベースから切断
            cursor.close()
            connector.close()

        return res


    '''
    指定されたユーザ、期間の稼働情報を削除する。
    入力値：
        userdata：(会社ID, アカウント, グループID, サブグループID）
        from_date：datetime.date
        to_date：datetime.date
    '''
    def delete_kadou(self, userdata, from_date=date.today(), to_date=date.today()):

        #SQL定義
        sql = '\
            DELETE FROM TBL_KADOU\
            WHERE\
                ACCOUNT = %s AND\
                DATE BETWEEN %s AND %s\
            '

        res = self.get_kadou(userdata, from_date, to_date)
        try:
            connector = mysql.connector.connect(**self.config)

            # SQL実行
            cursor = connector.cursor()
            cursor.execute(sql, (userdata[1], from_date.strftime('%Y/%m/%d'), to_date.strftime('%Y/%m/%d')))
            connector.commit()

        except mysql.connector.Error as e:
            print("Error:", e)
            print("Error:", str(e))
            res = { 'error': 'db connection error' }

        finally:
            # データベースから切断
            cursor.close()
            connector.close()

        return res

