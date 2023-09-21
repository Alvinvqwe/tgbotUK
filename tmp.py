# import telebot

# # 你的Telegram Bot的API令牌
# TOKEN = '6000416074:AAGD_1u1UaVIgn43Ld0BsGv1IpZcUc99qy8'

# # 初始化Telegram Bot
# bot = telebot.TeleBot(TOKEN)

# # 存储访客用户名的集合
# visitor_usernames = set()

# # 处理新消息
# @bot.message_handler(content_types=['text'])
# def handle_messages(message):
#     username = message.from_user.username
#     name = message.from_user.first_name
#     if message.from_user.last_name:
#         name = " ".join([message.from_user.first_name, message.from_user.last_name])
#     if username:
#         visitor_usernames.add("|".join([username, name]))
#     bot.send_message(message.from_user.id, "username 已录入")

# # 启动Bot
# bot.polling(none_stop=True)

# # 在这里可以将visitor_usernames保存到文件，去重操作已经在set中自动完成
# with open('visitor_usernames.txt', 'w') as file:
#     for username in visitor_usernames:
#         file.write(username + '\n')



#     



# from datetime import datetime, timedelta

# # 总年假天数
# total_annual_leave_days = 23

# # 总工作天数
# total_work_days = 260

# # 假设开始日期和结束日期（请根据实际情况修改）
# start_date = datetime(2023, 3, 1)
# end_date = datetime(2023, 9, 20)

# # 计算给定日期范围内的工作天数
# def calculate_work_days(start_date, end_date):
#     work_days = 0
#     current_date = start_date
#     while current_date <= end_date:
#         # 跳过周六和周日
#         if current_date.weekday() < 5:
#             work_days += 1
#         current_date += timedelta(days=1)
#     return work_days

# # 计算给定日期范围内的可申请年假天数
# def calculate_annual_leave_days(start_date, end_date, total_annual_leave_days, total_work_days):
#     work_days_in_range = calculate_work_days(start_date, end_date)
#     annual_leave_days_in_range = (work_days_in_range / total_work_days) * total_annual_leave_days
#     return annual_leave_days_in_range

# # 计算可申请年假天数
# annual_leave_days_for_range = calculate_annual_leave_days(start_date, end_date, total_annual_leave_days, total_work_days)

# # 输出结果
# print(f"在指定日期范围内（{start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}），可申请的年假天数为: {annual_leave_days_for_range:.2f} 天")




# 


import pymysql
from config import database

def connection():
    try:
        return pymysql.connect(host=database["host"],
            user=database["user"],
            password=database['password'],
            database=database['database'],
            charset=database['charset'],
            cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        raise e

def user_add(idemployee, username, firstname=" ", departmentID=0, chatid=None, lastname=None, isAdmin=0, lang="en"):
    if not idemployee or not username:
        return 0
    sql = f'INSERT INTO tgbotUK.employee (idemployee, chatid, username, departmentID, firstname, lastname, isAdmin, lang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    # print((idemployee, chatid, username, departmentID, firstname, lastname, isAdmin, lang))
    with conn.cursor() as cursor:
        cursor.execute(sql,(idemployee, chatid, username, departmentID, firstname, lastname, isAdmin, lang))
    conn.commit()
    return 1


dics = {"市场部": 1, "后勤部": 2, "行政部": 3, "财务部": 4, "审计部": 5, "人事部": 6, "赢创项目组": 7, "德星项目组": 8, "嘉华项目组": 9, "天宇项目组": 10, "Venus(Spring)": 11, "Mirror": 12, "Project X": 13}

# database connection init
conn = connection()

filename = './visitor_usernames.txt'

# Open the file in read mode
with open(filename, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Process the line (e.g., print it)
        print(line)  # .strip() removes newline characters at the end of each line
        tmpls = line.strip("\n").split("|")
        print(tmpls)
        user_add(idemployee=tmpls[3], username=tmpls[0], firstname=" ", departmentID=dics[tmpls[2]], chatid=None, lastname=None, isAdmin=0, lang="en")







