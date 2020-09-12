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
        messagebox.showerror('error','API.jsonファイルが存在しません。\n確認してください')
        return

    try: youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except:
        messagebox.showerror('error','APIキーが正しくないか存在しません。\n API.jsonファイルを確認してください')
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
    search_response = youtube.search().list(part='snippet',q=search_word,order=sort_value,type='channel')
    try:output = youtube.search().list(part='snippet',q=search_word,order=sort_value,type='channel').execute()
    except Exception as e:
        eee = str(e)
        if "Daily Limit Exceeded" in eee:
            messagebox.showinfo('info','本日の検索回数の上限に達しました\n日を跨いで実行して下さい')
            return
        else:
            messagebox.showerror('error','原因がわかりません。作成者に連絡して下さい。\n\n' + eee)
            return

    num = search_num // 5
    tag_list = []
    dic_list = []
    channel_get = []
    search_list = []
    channel_data_list = []
    columns_dic = {}
    channel_columns_dic = {}
    search_hantei = 0
    channel_hantei = 0

    #一度に5件しか取得できないため何度も繰り返して実行
    for i in range(num):
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()

    df = pd.DataFrame(dic_list)
    df_id = pd.DataFrame(list(df['id']))['channelId']    #各動画毎に一意のvideoIdを取得
    df_title = pd.DataFrame(list(df['snippet']))[['title']]    #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df_title = df_title.rename(columns = {'title':'チャンネル名'})

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
    columns_list = [df_title , df_tags]
    if Val_id.get() == True:columns_list.append(df_id)

    if Val_description.get() == True:
        search_list.append('description')
        columns_dic['description'] = 'チャンネルの概要'
        search_hantei += 1
    if Val_published.get() == True:
        search_list.append('publishedAt')
        columns_dic['publishedAt'] = 'チャンネル公開日'
        search_hantei += 1
    if Val_content.get() == True:
        search_list.append('liveBroadcastContent')
        columns_dic['liveBroadcastContent'] = 'ライブ配信の状態'
        search_hantei += 1
    if search_hantei >=1:
        df_detail = pd.DataFrame(list(df['snippet']))[search_list]
        df_detail = df_detail.rename(columns = columns_dic)
        columns_list.append(df_detail)

    if Val_scriber_count.get() == True:
        channel_data_list.append('subscriberCount')
        channel_columns_dic['subscriberCount'] = 'チャンネル登録者数'
        channel_hantei += 1
    if Val_video_count.get() == True:
        channel_data_list.append('videoCount')
        channel_columns_dic['videoCount'] = '投稿動画数'
        channel_hantei += 1
    if Val_view_count.get() == True:
        channel_data_list.append('viewCount')
        channel_columns_dic['viewCount'] = '動画総再生数'
        channel_hantei += 1
    if channel_hantei >= 1:
        for channel_id in df_id:
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            channel_response = youtube.channels().list(part='statistics',id=channel_id).execute()
            test = channel_response['items'][0]['statistics']['hiddenSubscriberCount']
            if test == True: channel_response['items'][0]['statistics']['subscriberCount']="非公開"
            channel_get = channel_get + channel_response['items']
        df1 = pd.DataFrame(channel_get)['statistics']
        df_channel = pd.DataFrame(list(df1))[channel_data_list]
        df_channel = df_channel.rename(columns = channel_columns_dic)
        columns_list.append(df_channel)

    df_result = pd.concat(columns_list, axis = 1)
    df_result.to_csv('{}.csv'.format(search_word) , header=True)
    messagebox.showinfo('info','処理が完了しました。')

def Clear():exit()

root = tkinter.Tk()
root.title(u"youtube チャンネル検索")
root.geometry("380x360")

label_word = tkinter.Label(text=u'検索ワード：')
label_word.place(x = 35 , y = 13)
label_search_num = tkinter.Label(text=u'検索数(5件刻み)：')
label_search_num.place(x = 5 , y = 53)
label_search_item = tkinter.Label(text=u'［検索項目］')
label_search_item.place(x = 5 , y = 95)
label_sort = tkinter.Label(text=u'［ソート順］')
label_sort.place(x = 5 , y = 230)
Editbox_word = tkinter.Entry(text=u'検索ワード：',width=26) #検索ワード
Editbox_word.place(x=118 , y=10)
Editbox_search_num = tkinter.Entry(width=5) #検索数
Editbox_search_num.insert(tkinter.END,"5")
Editbox_search_num.place(x=118 , y=50)

valuelist=["視聴回数が多い順","評価が高い順","作成日が新しい順","関連度が高い順番","アルファベット順"]  #選択肢リスト
valuedic={'作成日が新しい順':'date','評価が高い順':'rating','関連度が高い順番':'relevance','アルファベット順':'title','視聴回数が多い順':'viewCount'}
combo=ttk.Combobox(root , values=valuelist)
combo.current(0)
combo.place(x = 30 , y = 255)

Val_description = tkinter.BooleanVar()
Val_published = tkinter.BooleanVar()
Val_id = tkinter.BooleanVar()
Val_content = tkinter.BooleanVar()
Val_scriber_count = tkinter.BooleanVar()
Val_video_count = tkinter.BooleanVar()
Val_view_count = tkinter.BooleanVar()
Val_description.set(True)
Val_published.set(True)
Val_id.set(True)
Val_content.set(True)
Val_scriber_count.set(True)
Val_video_count.set(True)
Val_view_count.set(True)
description_box = tkinter.Checkbutton(root , text=u"チャンネルの概要" , variable = Val_description)
description_box.place(x = 30 , y = 120)
published_box = tkinter.Checkbutton(root , text=u"チャンネル公開日" , variable = Val_published)
published_box.place(x = 170 , y = 120)
id_box = tkinter.Checkbutton(root , text=u"チャンネルID" , variable = Val_id)
id_box.place(x = 30 , y = 145)
content_box = tkinter.Checkbutton(root , text=u"ライブ配信の状態" , variable = Val_content)
content_box.place(x = 170 , y = 145)
scriber_count_box = tkinter.Checkbutton(root , text=u"チャンネル登録者数" , variable = Val_scriber_count)
scriber_count_box.place(x = 30 , y = 170)
video_count_box = tkinter.Checkbutton(root , text=u"投稿動画数" , variable = Val_video_count)
video_count_box.place(x = 170 , y = 170)
view_count_box = tkinter.Checkbutton(root , text=u"動画総再生回数" , variable = Val_view_count)
view_count_box.place(x = 30 , y = 195)

Button_enter = tkinter.Button(text=u'検索' , width=15 , command = get_video_info)
Button_enter.place(x = 30 , y = 320)
Button_clear = tkinter.Button(text=u'終了' , width=15 , command = Clear)
Button_clear.place(x = 210,y = 320)

if __name__ == "__main__":
    root.mainloop()
