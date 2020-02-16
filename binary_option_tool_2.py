import glob
import tkinter
from tkinter import Tk
import data_analyze_2 as da
from tkinter import messagebox

def GetEntryValue():
    where_list = []
    where_value = "where "

    value_year = EditBox_year.get()
    if value_year == "":where_list.append("")
    else:where_list.append("year = " + value_year)

    value_month = EditBox_month.get()
    if value_month == "":where_list.append("")
    else:where_list.append("month = " + value_month)

    value_week = EditBox_week.get()
    if value_week == "":where_list.append("")
    else:where_list.append("weeks = " + value_week)

    value_dow = EditBox_dow.get()
    if value_dow == "Mon" or value_dow == "Tue" or value_dow == "Wed" or value_dow == "Thi" or value_dow == "Fri" or value_dow == "":
        if value_dow == "":where_list.append("")
        else:where_list.append("WOD = " + "'" + value_dow + "'")
    else:messagebox.showerror("title" , "正しい「年」の値を入力してください。(Mon , Tue , Wed , Thi , Fri)")

    if value_year == "" and value_month == "" and value_week == "" and value_dow == "":
        where_value = ''
    else:
        for i in where_list:
            if where_value == "where ":where_value = where_value + i
            else:
                if i == "":pass
                else:where_value = where_value + " and " + i

    result , point , win , lose = da.win_rate(where_value)

    result_win.set(win)
    result_lose.set(lose)
    result_point.set(point)
    result_winrate.set(result)

def Clear():
    EditBox_year.delete('0' , 'end')
    EditBox_month.delete('0' , 'end')
    EditBox_week.delete('0' , 'end')
    EditBox_dow.delete('0' , 'end')
    result_win.set("")
    result_lose.set("")
    result_point.set("")
    result_winrate.set("")

root = tkinter.Tk()
root.title(u"data_analyze_GUI")
root.geometry("380x240")

result_win = tkinter.IntVar(value = "")
result_lose = tkinter.IntVar(value = "")
result_point = tkinter.IntVar(value = "")
result_winrate = tkinter.IntVar(value = "")

label_year = tkinter.Label(text=u'  年：')
label_year.place(x = 10 , y = 10)
label_month = tkinter.Label(text=u'  月：')
label_month.place(x = 10 , y = 50)
label_week = tkinter.Label(text=u'  週：')
label_week.place(x = 10 , y = 90)
label_dow = tkinter.Label(text=u'曜日：')
label_dow.place(x = 10 , y = 130)
label_win = tkinter.Label(text=u'勝ち：')
label_win.place(x = 190 , y = 10)
label_lose = tkinter.Label(text=u'負け：')
label_lose.place(x = 190 , y = 50)
label_point = tkinter.Label(text=u'収支：')
label_point.place(x = 190 , y = 90)
label_winrate = tkinter.Label(text=u'勝率[%]：')
label_winrate.place(x = 170 , y = 130)

EditBox_year = tkinter.Entry(width=10)
EditBox_year.place(x=50 , y=10)
EditBox_month = tkinter.Entry(width=10)
EditBox_month.place(x=50 , y=50)
EditBox_week = tkinter.Entry(width=10)
EditBox_week.place(x=50 , y=90)
EditBox_dow = tkinter.Entry(width=10)
EditBox_dow.place(x=50 , y=130)
EditBox_win = tkinter.Entry(root , textvariable = result_win , width=10 , fg="#000000" , bg="#ffffff")
EditBox_win.place(x=230 , y=10)
EditBox_lose = tkinter.Entry(root , textvariable = result_lose , width=10 , fg="#000000" , bg="#ffffff")
EditBox_lose.place(x=230 , y=50)
EditBox_point = tkinter.Entry(root , textvariable = result_point , width=10 , fg="#000000" , bg="#ffffff")
EditBox_point.place(x=230 , y=90)
EditBox_winrate = tkinter.Entry(root , textvariable = result_winrate , width=10 , fg="#000000" , bg="#ffffff")
EditBox_winrate.place(x=230 , y=130)

Button_enter = tkinter.Button(text=u'Enter' , width=15 , command = GetEntryValue)
Button_enter.place(x = 30 , y = 200)
Button_clear = tkinter.Button(text=u'Clear' , width=15 , command = Clear)
Button_clear.place(x = 210,y = 200)

if __name__ == "__main__":
    root.mainloop()