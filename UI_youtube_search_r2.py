import json
import tkinter
from tkinter import Tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pandas as pd
import lxml.html as lx
import requests as re
from apiclient.discovery import build

def get_video_info():   #part, q, order, type, num
    try:
        json_open = open('API.json', 'r')
        json_load = json.load(json_open)
        YOUTUBE_API_KEY = json_load["API_KEY"]
    except:
        messagebox.showinfo('info','API.jsonファイルが存在しません。\n確認してください')
        return

    try: youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except:
        messagebox.showinfo('info','APIキーが正しくないか存在しません。\n API.jsonファイルを確認してください')
        return

    search_word = Editbox_word.get()
    if search_word == '':
        messagebox.showinfo('info','検索ワードを入力してください')
        return

    search_num = Editbox_search_num.get()
    if search_num == '':
        messagebox.showinfo('info','検索数を入力して下さい（5件刻み）')
        return

    try:search_num = int(search_num)
    except:
        messagebox.showinfo('info','検索数には半角数字を入力して下さい（5件刻み）')
        return

    sort_value = valuedic[combo.get()]
    num = search_num // 5
    tag_list = []
    dic_list = []
    search_list = []
    columns_dic = {}

    if Val_description.get() == True:
        search_list.append('description')
        columns_dic['description'] = 'チャンネルの詳細'
    if Val_published.get() == True:
        search_list.append('publishedAt')
        columns_dic['publishedAt'] = 'チャンネル公開日'
    if Val_content.get() == True:
        search_list.append('liveBroadcastContent')
        columns_dic['liveBroadcastContent'] = 'ライブ配信の状態'

    search_response = youtube.search().list(part='snippet',q=search_word,order=sort_value,type='channel')
    try:output = youtube.search().list(part='snippet',q=search_word,order=sort_value,type='channel').execute()
    except Exception as e:
        eee = str(e)
        if "Daily Limit Exceeded" in eee:
            messagebox.showinfo('info','本日の検索回数の上限に達しました\n日を跨いで実行して下さい')
            return
        else:
            messagebox.showinfo('error','原因がわかりません。作成者に連絡して下さい。\n\n' + eee)
            return

    #一度に5件しか取得できないため何度も繰り返して実行
    for i in range(num):
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()

    df = pd.DataFrame(dic_list)
    df_id = pd.DataFrame(list(df['id']))['channelId']    #各動画毎に一意のvideoIdを取得
    df_title = pd.DataFrame(list(df['snippet']))[['title']]    #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df_title = df_title.rename(columns = {'title':'チャンネル名'})
    df_detail = pd.DataFrame(list(df['snippet']))[search_list]
    df_detail = df_detail.rename(columns = columns_dic)

    for id in df_id:
        target_url = 'https://www.youtube.com/channel/' + id + '/channels'
        html = re.get(target_url).text
        dom = lx.fromstring(html)
        tag_tmp = dom.xpath('//meta[@property="og:video:tag"]')

        tmp = ''
        for i in tag_tmp:
            channel_tag = str(i.attrib)
            tmp = tmp + channel_tag[41:-2] + " "
        tag_tmp.clear()
        tag_list.append(tmp)

    df_tags = pd.DataFrame(tag_list , columns=['チャンネルタグ'])
    if Val_id.get() == True:df_result = pd.concat([df_title , df_tags , df_id , df_detail], axis = 1)
    else: df_result = pd.concat([df_title , df_tags , df_detail], axis = 1)
    df_result.to_csv('{}.csv'.format(search_word) , header=True)
    messagebox.showinfo('info','処理が完了しました。')

def Clear():exit()

root = tkinter.Tk()
root.title(u"youtube チャンネル検索")
root.geometry("380x310")

label_word = tkinter.Label(text=u'検索ワード：')
label_word.place(x = 35 , y = 13)
label_search_num = tkinter.Label(text=u'検索数(5件刻み)：')
label_search_num.place(x = 5 , y = 53)
label_search_item = tkinter.Label(text=u'［検索項目］')
label_search_item.place(x = 5 , y = 95)
label_sort = tkinter.Label(text=u'［ソート順］')
label_sort.place(x = 5 , y = 180)
Editbox_word = tkinter.Entry(text=u'検索ワード：',width=26) #検索ワード
Editbox_word.place(x=118 , y=10)
Editbox_search_num = tkinter.Entry(width=5) #検索数
Editbox_search_num.insert(tkinter.END,"5")
Editbox_search_num.place(x=118 , y=50)

valuelist=["チャンネルの動画総再生数","評価が高い順","作成日が新しい順","関連度が高い順番","アルファベット順"]  #選択肢リスト
valuedic={'作成日が新しい順':'date','評価が高い順':'rating','関連度が高い順番':'relevance','アルファベット順':'title','チャンネルの動画総再生数':'viewCount'}
combo=ttk.Combobox(root , values=valuelist)
combo.current(0)
combo.place(x = 30 , y = 205)

Val_description = tkinter.BooleanVar()
Val_published = tkinter.BooleanVar()
Val_id = tkinter.BooleanVar()
Val_content = tkinter.BooleanVar()
Val_description.set(True)
Val_published.set(True)
Val_id.set(True)
Val_content.set(True)
description_box = tkinter.Checkbutton(root , text=u"チャンネルの概要" , variable = Val_description)
description_box.place(x = 30 , y = 120)
published_box = tkinter.Checkbutton(root , text=u"チャンネル公開日" , variable = Val_published)
published_box.place(x = 170 , y = 120)
id_box = tkinter.Checkbutton(root , text=u"チャンネルID" , variable = Val_id)
id_box.place(x = 30 , y = 145)
content_box = tkinter.Checkbutton(root , text=u"ライブ配信の状態" , variable = Val_content)
content_box.place(x = 170 , y = 145)

Button_enter = tkinter.Button(text=u'検索' , width=15 , command = get_video_info)
Button_enter.place(x = 30 , y = 270)
Button_clear = tkinter.Button(text=u'終了' , width=15 , command = Clear)
Button_clear.place(x = 210,y = 270)

if __name__ == "__main__":
    root.mainloop()