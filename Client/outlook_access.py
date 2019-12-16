# coding: utf-8
from datetime import datetime, timedelta, date
import win32com.client as wcl


class OutlookScheduleAccess:

    '''
    コンストラクタ
    Outlookのフォルダ情報を設定する。
    '''
    def __init__(self):
        namespace = wcl.Dispatch('Outlook.Application').GetNamespace('MAPI')
        # Outlookフォルダを設定する
        self.folder = namespace.GetDefaultFolder(9) #olFolderCalendar

        # Outlookのユーザ名を取得する。 -> ABC 山田 太朗/Yamada, Taro (Company Name)
        username = namespace.CurrentUser.Name
        # 氏名を設定する。
        self.name = username[4:username.find('/')]


    '''
    指定した期間（日付）でWBSコードが含まれるのOutlookの予定をディクショナリのリスト形式で取得する。
    デフォルト値は実行日とする。
    返却値：
        {[
            'start': 予定開始時間(datetime.datetime),
            'end': 予定修了時間(datetime.datetime),
            'date': 予定日付(datetime.date),
            'delta': 予定期間(datetime.timedelta),
            'wbscode': WBSコード(string) <業務ID-イベントID-Lカテゴリ-Mカテゴリ-Sカテゴリ-VSカテゴリ>　例：<10-1-10-10-10-1>
            'comment': コメント(string)
        ],[],[], ...}   
    '''
    def get_schedule(self, from_date=date.today(), to_date=date.today()):
        schedule_list = []
        for item in self.folder.Items:
            item_start = self.pywintypes_to_datetime(item.Start)
            item_end = self.pywintypes_to_datetime(item.End)
            item_subject = item.Subject.replace('\u3000','')

            # 指定期間外の場合は取得しない。
            item_date = item_start.date()        
            if item_date < from_date or to_date < item_date:
                continue

            # WBSコードが指定されていない場合は取得しない。        
            from_index = item_subject.find('<')
            to_index = item_subject.find('>')
            if from_index < 0 or to_index < 0 or to_index < from_index:
                continue

            # WBSコードの要素数が6でない場合は取得しない。
            wbscode = item_subject[from_index+1:to_index].split('-')
            if len(wbscode) != 6:
                continue

            schedule = {
                'start': item_start,
                'end': item_end,
                'date': item_start.date(),
                'delta': item_end - item_start,
                'wbscode': item_subject[from_index+1:to_index].split('-'),
                'comment': item_subject[to_index+1:]
            }
            schedule_list.append(schedule)
        
        return schedule_list


    '''
    スケジュールリストの各要素について、予定時間の重複排除を行う。
    重複している場合は、予定の長さが長い方を選択する。
    '''
    def deduplicate_schedule(self, schedule_list):
        # 予定を並び替える。（第一キー：日付、第二キー：予定の長さ）
        schedule_list_sort = sorted(schedule_list, key=lambda x: (x['date'], x['delta'], x['start']))

        # 重複排除したスケジュールリストを作成する。
        deduplicated_schedule = []
        for x in range(len(schedule_list_sort)):

            # 最終項目の場合は要素を追加する。
            schedule = schedule_list_sort[x]
            if x == len(schedule_list_sort) - 1:
                deduplicated_schedule.append(schedule)
                continue
            
            # 他の予定との重複を確認し、重複していなければ予定を登録する。
            isDuplicate = False
            for y in range(x + 1, len(schedule_list_sort)):
                # 日付が異なる場合、以降の要素は重複なしと判断
                if schedule['date'] != schedule_list_sort[y]['date']:
                    break
                # 予定の重複を確認
                if self.isDuplicate(schedule, schedule_list_sort[y]):
                    isDuplicate = True
                    break
            
            if isDuplicate:
                continue
            else:
                deduplicated_schedule.append(schedule)

        return deduplicated_schedule


    '''
    2つの予定について、予定が重複しているかどうかを検査する。
    重複している場合はTrue、重複していない場合はFalseを返す
    '''
    def isDuplicate(self, schedule1, schedule2):
        # 重複なし
        if schedule1['end'] <= schedule2['start'] or schedule2['end'] <= schedule1['start']:
            return False
        # 重複あり
        return True


    '''
    pywintypes.datetimeをdatetime.datetimeに変換する。
    '''
    def pywintypes_to_datetime(self, d):
        return datetime.utcfromtimestamp(d.timestamp())

