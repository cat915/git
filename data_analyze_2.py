import mysql.connector as mydb
from decimal import Decimal

def win_rate(where_value):
    win = Decimal('0.00')
    lose = 0

    # コネクションの作成
    conn = mydb.connect(
        host='takeuchiyuugo-no-MacBook-Air.local',
        port='3306',
        user='root',
        password='sanfredaisuki5',
        database='test'
    )

    # コネクションが切れた時に再接続してくれるよう設定
    conn.ping(reconnect=True)

    # 接続できているかどうか確認
    if conn.is_connected() == False:
        print("SQLサーバーと接続できません。条件を確認してください")
    elif conn.is_connected() == True:
        print("接続成功!!")

    # DB操作用にカーソルを作成
    cur = conn.cursor()

    # データの参照（select)
    cur.execute("SELECT win , lose FROM binary_option {}".format(where_value))

    # 全てのデータを取得
    rows = cur.fetchall()

    for row in rows:
        if row[0] == None:
            pass
        else:
            win = win + row[0]
            lose = lose + row[1]

    if win == None:
        result = None
        point = None
    else:
        win = float(win)
        point = round(win * 0.88 - lose , 1)
        result = round(win / (win + lose) * 100 , 1)
        win = round(win , 1)
    return result , point , win , lose