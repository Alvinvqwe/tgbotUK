from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import types
import model
import config
from datetime import datetime

class employeeStates(StatesGroup):
	# statesgroup should contain states
    user_info = State()
    # chat_id = State()
    # username = State()

# tg bot init
bot = AsyncTeleBot(config.TELEBOT_BOT_TOKEN, state_storage=StateMemoryStorage())

# authorication
async def auth(data):
	# check chatid
	chat_id = data.from_user.id
	res, user_ = model.auth_(chat_id)
	# print(user_)
	if not res:
		res_, data_ = model.authByUsername(data.from_user.username)
		if res_:
			# if the first time login
			model.user_update(
				chat_id=chat_id, 
				username=data.from_user.username,
				firstname=data.from_user.first_name,
				lastname=data.from_user.last_name,
				isRegister=True
			)
			return True, data_[0]
		else:
			# users if not valid
			await bot.send_message(chat_id, text=config.lang["en"]["auth_faild"])
			return None, None
	else:
		# check if username and firstname/lastname have been updated
		username = data.from_user.username if data.from_user.username != user_[0]["username"] else None
		firstname = data.from_user.first_name if data.from_user.first_name != user_[0]["firstname"] else None
		lastname = data.from_user.last_name if data.from_user.last_name != user_[0]["lastname"] else None
		model.user_update(
				chat_id=chat_id, 
				username=username,
				firstname=firstname,
				lastname=lastname,
				isRegister=False
			)
		return True, user_[0]


# admin
# if so, Enable the section
async def isAdmin(data):
	# check chatid
	chat_id = data.from_user.id
	res, user_ = model.auth_(chat_id, isAdmin=1)
	if not res:
		# await bot.send_message(chat_id, text=config.lang["en"]["auth_admin_faild"]+config.lang["cn"]["auth_admin_faild"])
		return False
	return True


# default commands list
def commands_list():
	pass


########################## 
# utils funcs

# lang set function
def lang_set_keyboard():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.add("English", "中文")
	return keyboard

# dispart the menu configs json and return the right section
def render_menu(menu_id, action=1, lang_set="en", isAdmin=False):
	title = config.lang[lang_set]["menu"]
	cfg = config.menu
	if isAdmin:
		cfg[4]["Enable"] = True
	# print("menu_id: ", menu_id)
	if action:
		# action in
		for i in menu_id:
			title = cfg[int(i)]["display"][lang_set]
			cfg = cfg[int(i)]["submenu"]
	else:
		# action back
		# print(menu_id, menu_id[:-1])
		if len(menu_id)>1:
			for i in menu_id[:-1]:
				title = cfg[int(i)]["display"][lang_set]
				cfg = cfg[int(i)]["submenu"]
			
	return title, cfg


# render the keyboard
def menu_keyboard(config, index="0", lang="en", back=0, action=1):
	keyboard_ = []
	for i in config:
		if i["Enable"]:
			# web_app = None
			# if "link" in i and len(i["link"])>1:
			# 	web_app = types.WebAppInfo(url=i["link"]) 
			# print(web_app)
			keyboard_.append([
				types.InlineKeyboardButton(
					text=i['display'][lang],
					callback_data=func_menu.new(menu_id=i["id"])
					# web_app=web_app,
				)
			])
	if back:
		if not action: index=index[:-1]
		keyboard_.append([
			types.InlineKeyboardButton(
					text='⬅',
					callback_data="back_%s"%index
				)
		])
	return types.InlineKeyboardMarkup(keyboard = keyboard_)


########################## 
# callbacks list
func_menu = CallbackData('menu_id', prefix='funcs')

class MenuCallbackFilter(AdvancedCustomFilter):
	key = 'config'

	async def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
		return config.check(query=call)

# call center for the menu
# Any other menu items
@bot.callback_query_handler(func=None, config=func_menu.filter())
async def menu_callback(call: types.CallbackQuery):
	res_, user = await auth(data=call)
	chat_id = call.message.chat.id
	if not res_: 
		await bot.send_message(call.message.chat.id, text=config.lang[dics[message.text]]["lang_set_succeed"])
		return;
	callback_data: dict = func_menu.parse(callback_data=call.data)

	menu_id = int(callback_data['menu_id'])
	res = callback_data['menu_id']
	lang = user["lang"]

	# print(res)

	clock_code_m = { "41000": 3, "41001": 4, "41002": 5, "41003": 6, "41004": 7, "41005": 8, "41006": 9, "41007": 10, "41008": 11, "41009": 12 }
	clock_code_d = { "41100": 3, "41101": 4, "41102": 5, "41103": 6, "41104": 7, "41105": 8, "41106": 9, "41107": 10, "41108": 11, "41109": 12 }
	employees_ls = { "4330": -1, "4331": 3, "4332": 4, "4333": 5, "4334": 6, "4335": 7, "4336": 8, "4337": 9, "4338": 10, "4339": 11, "433x": 12,  }

	# print(res)
	# lang set func in menu
	if res in ["300", "301"]:
		# 300 cn
		# 301 en
		dics = {"300": "cn", "301": "en"}
		try:
			model.lang_set(call.message.chat.id, dics[res])
		except Exception as e:
			raise e
		# finally:
		await bot.send_message(call.message.chat.id, text=config.lang[dics[res]]["lang_set_succeed"])
		# update the keyboard
		title, cfg = render_menu(res[:-1], action=0, lang_set=lang, isAdmin=await isAdmin(data=call))
		back = 0 if title in [config.lang["cn"]["menu"], config.lang["en"]["menu"]] else 1
		keyboard = menu_keyboard(config=cfg, index=res[:-1], lang=dics[res], back=back, action=0)
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
						text=title, reply_markup=keyboard)

	# clock
	elif res in ["00"]:
		web_app = types.WebAppInfo(url='https://www.tgbotuktrinity.space/?'+"chatid="+str(call.message.chat.id))
		# print(web_app)
		button_c_in = types.InlineKeyboardButton('clock', web_app=web_app)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(button_c_in)
		await bot.send_message(call.message.chat.id, text='clock link/打卡链接', reply_markup=keyboard)

	elif res in ["011", "012"]:
		range_ = "month" if res == "012" else "day"
		tmp_res, data = model.clock_check(user["idemployee"], range_=range_)

		if not tmp_res:
			# 无记录
			await bot.send_message(call.message.chat.id, text="no records/没有记录")
		else:
			reply_text = []
			for i in data:
				reply_text.append("|".join([i["officeName"], str(i["clockin"]), str(i["clockout"])]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n".join(reply_text))

	# posts
	elif res in ["10", "11"]:
		# 10 latest
		if res == "10":
			tmp_res, data = model.posts_list(num=1)
			print(data)
			reply_text = []
			for i in data:
				reply_text.append("---".join([i["content"], str(i["post_date"])]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n".join(reply_text))

		# 11 history
		if res == "11":
			tmp_res, data = model.posts_list(num=5)
			reply_text = []
			for i in data:
				reply_text.append("---".join([i["content"], str(i["post_date"])]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n".join(reply_text))

	# report
	elif res in ["20", "22"]:
		# make a IT issues report
		if res == "20":
			await bot.send_message(call.message.chat.id, text=config.lang[lang]["report_intro"])

		# search report history by employee
		if res == "22":
			tmp_res, data = model.report_list(user["idemployee"])
			reply_text = []
			for i in data:
				reply_text.append("---".join(i[["content"], str(i["date"])]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n".join(reply_text))

	################
	# admin section
	################

	# clock section
	# by month
	elif res in clock_code_m.keys():
		tmp_res, data = model.clocks_report(clock_code_m[res], range_="month")
		reply_text = []
		for i in data:
			reply_text.append("|".join([i["employeeID"], i["username"], i["officeName"]]) + "\nCLOCK IN:" + str(i["clockin"]) + "\nCLOCK OUT:" + str(i["clockout"]))
		if not reply_text: 
			reply_text=["no records/没有记录"]
		await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))

	# search by monthly history for all
	elif res == "4101":
		tmp_res, data = model.clocks_report(range_="month")
		reply_text = []
		for i in data:
			reply_text.append("|".join([i["employeeID"], "@"+i["username"], i["officeName"]]) + "\nCLOCK IN:" + str(i["clockin"]) + "\nCLOCK OUT:" + str(i["clockout"]))
		if not reply_text: 
			reply_text=["no records/没有记录"]
		await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))

	# by day
	elif res in clock_code_d.keys():
		tmp_res, data = model.clocks_report(clock_code_d[res], range_="day")
		reply_text = []
		for i in data:
			reply_text.append("|".join([i["employeeID"], i["username"], i["officeName"]]) + "\nCLOCK IN:" + str(i["clockin"]) + "\nCLOCK OUT:" + str(i["clockout"]))
		if not reply_text: 
			reply_text=["no records/没有记录"]
		await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))

	# search by daily history for all
	elif res == "4111":
		tmp_res, data = model.clocks_report(range_="day")
		reply_text = []
		for i in data:
			reply_text.append("|".join([i["employeeID"], i["username"], i["officeName"]]) + "\nCLOCK IN:" + str(i["clockin"]) + "\nCLOCK OUT:" + str(i["clockout"]))
		if not reply_text: 
			reply_text=["no records/没有记录"]
		await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))

	elif res in ["40"]:
		# report section
		if res == "40":
			tmp_res, data = model.report_list()
			reply_text = []
			for i in data:
				reply_text.append("---".join([i["content"], i["date"]]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))

	# posts management section
	elif res in ["420", "421"]:
		# make a post
		if res == "420":
			# /makeAnReport_IT
			await bot.send_message(call.message.chat.id, text=config.lang[lang]["post_intro"])

		# check posts list for all
		if res == "421":
			tmp_res, data = model.posts_list(num=0)
			reply_text = []
			for i in data:
				reply_text.append("---".join([i["content"], i["date"]]))
			if not reply_text: 
				reply_text=["no records/没有记录"]
			await bot.send_message(call.message.chat.id, text="\n------\n".join(reply_text))
			

	elif res in ["430", "431", "432"]:
		# employees management section
		# add
		if res == "430":
			# /add_user
			await bot.send_message(call.message.chat.id, text=config.lang[lang]["add_user"])
			await bot.send_message(chat_id, text=config.lang["cn"]["department_ls"])

		# remove
		if res == "431":
			# remove(idemployee):
			# /remove_user
			await bot.send_message(call.message.chat.id, text=config.lang[lang]["remove_user"])

		# update
		if res == "432":
			# user_update(chat_id, username=None, firstname=None, lastname=None, isRegister=False):
			# /update_user
			await bot.send_message(call.message.chat.id, text=config.lang[lang]["update_user"])
			await bot.send_message(chat_id, text=config.lang["cn"]["department_ls"])

	# check employees list by departments
	elif res in employees_ls.keys():
		tmp_res, data = model.user_list(department_id=employees_ls[res])
		reply_text = []
		for i in data:
			name = i["firstname"] if not i["lastname"] else i["firstname"] + i["lastname"]
			reply_text.append("|".join([i["idemployee"], "@"+i["username"], name, i["departmentName"]]))
		if not reply_text: 
			reply_text=["no records/没有记录"]
		await bot.send_message(call.message.chat.id, text="\n".join(reply_text))

	else:
		# direct to the section configs
		title, cfg = render_menu(callback_data['menu_id'], action=1, lang_set=lang, isAdmin=await isAdmin(data=call))
		back = 0 if title in [config.lang["cn"]["menu"], config.lang["en"]["menu"]] else 1
		keyboard = menu_keyboard(config=cfg, index=res, lang=lang, back=back, action=1)
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
				text=title, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
async def menu_command_handler(message):
	res_, user = await auth(data=message)
	if not res_: return;
	res = message.data
	# print(res)
	lang = user["lang"]
	index = res.split("_")[-1]
	# get the section configs
	title, cfg = render_menu(index, action=0, lang_set=lang, isAdmin=await isAdmin(data=message))
	# print(cfg)
	back = 0 if title in [config.lang["cn"]["menu"], config.lang["en"]["menu"]] else 1
	keyboard = menu_keyboard(config=cfg, index=index, lang=user["lang"], back=back, action=0)
	await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
						text=title, reply_markup=keyboard)


# lang set callback
@bot.message_handler(content_types=["text"], func=lambda message: message.text in ["English", "中文"])
async def lang_set(message):
	res, user = await auth(data=message)
	if not res: return;
	chat_id = message.from_user.id
	dics = {"English": "en", "中文": "cn"}
	try:
		model.lang_set(chat_id, dics[message.text])
	except Exception as e:
		raise e
	# finally:
	await bot.send_message(chat_id, text=config.lang[dics[message.text]]["lang_set_succeed"])
	# send the funcs menu by lang selected
	cfg = config.menu
	res_tmp = await isAdmin(data=message)
	if res_tmp:
		cfg[4]["Enable"] = True
	await bot.send_message(message.chat.id, text=config.lang[dics[message.text]]["menu"], 
		reply_markup=menu_keyboard(config=cfg, index="0", lang=dics[message.text], back=0, action=1))


########################## 
# commands list
@bot.message_handler(commands=["update_user"])
async def update_user_command_handler(message):
	# res, user = await auth(data=message)
	# if not res: return;
	# if not await isAdmin(data=message): return;

	# chat_id = message.from_user.id
	# tmp_res = message.text.split()[1:]
	# print(tmp_res)

	# if not tmp_res:
	# 	await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	# else:
	# 	user_init_info = " ".join(tmp_res).split(" ")
	# 	info_username = user_init_info.pop(0)
	# 	# check username if valid
	# 	user_res, user_info = model.authByUsername(info_username)
	# 	if not user_res:
	# 		await bot.send_message(chat_id, text=config.lang[user["lang"]]["check_user"])
	# 		return

	# 	# params
	# 	print()
	# 	params_ls = {"employeeID": None, "departmentID": None}
	# 	for i in user_init_info:
	# 		params = i.split(":")
	# 		if len(params)!=2:
	# 			await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	# 			return
	# 		if params[0] in ["employeeID", "departmentID"]:
	# 			params_ls[params[0]] = params[1]

	# 	action_res = model.user_update_info(username=info_username, employeeID=params_ls["employeeID"], departmentID=params_ls["departmentID"])
	# 	if action_res:
	# 		await bot.send_message(chat_id, text=config.lang[user["lang"]]["task_done"])
	# 	else:
	# 		await bot.send_message(chat_id, text=config.lang[user["lang"]]["params_err"])
	await bot.send_message(message.from_user.id, text="很抱歉，功能目前还在优化中，暂未开放")


@bot.message_handler(commands=["remove_user"])
async def remove_user_command_handler(message):
	# res, user = await auth(data=message)
	# if not res: return;
	# if not await isAdmin(data=message): return;
	# chat_id = message.from_user.id
	# tmp_res = message.text.split()[1:]
	# if not tmp_res:
	# 	await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	# else:
	# 	if model.remove_user(idemployee=tmp_res):
	# 		await bot.send_message(chat_id, text=config.lang[user["lang"]]["task_done"])
	# 	else:
	# 		await bot.send_message(chat_id, text=config.lang[user["lang"]]["sys_err"])
	await bot.send_message(message.from_user.id, text="很抱歉，功能目前还在优化中，暂未开放")


@bot.message_handler(commands=["add_user"])
async def add_user_command_handler(message):
	res, user = await auth(data=message)
	if not res: return;
	if not await isAdmin(data=message): return;
	chat_id = message.from_user.id
	tmp_res = message.text.split()[1:]
	if not tmp_res:
		await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	else:
		user_init_info = " ".join(tmp_res).split(":")
		if len(user_init_info)!=3:
			await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
		else:
			# user_add(idemployee, username, firstname, departmentID=0, chatid=None, lastname=None, isAdmin=0, lang="en"):
			# await bot.send_message(chat_id, text=config.lang["en"]["department_ls"])
			model.user_add(idemployee=user_init_info[0], username=user_init_info[1], firstname=" ", departmentID=int(user_init_info[2]), chatid=None, lastname=None, isAdmin=0, lang="en")
			# done alert msg
			await bot.send_message(chat_id, text=config.lang[user["lang"]]["task_done"])


@bot.message_handler(commands=["makeAnPost"])
async def post_command_handler(message):
	res, user = await auth(data=message)
	if not res: return;
	if not await isAdmin(data=message): return;
	chat_id = message.from_user.id
	tmp_res = message.text.split()[1:]
	if not tmp_res:
		await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	else:
		# save it into the database
		content = " ".join(tmp_res)
		# add_post(ctx, date, publisher_chatid, type_=0, attaches=None)
		date_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		model.add_post(ctx=content, post_date=date_, publisher_chatid=chat_id, post_type=0, attaches=None)
		user_ls, data = model.user_list()
		print(data)
		for i in data:
			if i["chatid"]:
				# transfer the msg the user group that selected
				await bot.send_message(i["chatid"], text=content)

		# done alert msg
		await bot.send_message(chat_id, text=config.lang[user["lang"]]["task_done"])


@bot.message_handler(commands=["makeAnReport_IT"])
async def reportIT_command_handler(message):
	res, user = await auth(data=message)
	if not res: return;
	chat_id = message.from_user.id
	tmp_res = message.text.split()[1:]
	if not tmp_res:
		await bot.send_message(chat_id, text=config.lang[user["lang"]]["empty_warn"])
	else:
		# save it into the database
		content = " ".join(tmp_res)
		# (idemployee, content, date, type_=0)
		date_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		model.make_report(user["idemployee"], content, date_, type_=0)
		# transfer the msg to the chatid of Alvin
		issues = [f'from {user["username"]}', content, f'report time: {date_}']
		await bot.send_message(config.chatID_ls["IT_support"], text="\n".join(issues))

@bot.message_handler(commands=['start'])
async def greeting(message):
	res, user = await auth(data=message)
	if not res: return;
	chat_id = message.from_user.id
	keyboard = lang_set_keyboard()
	sent_msg = await bot.send_message(chat_id, text='please select a language', reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
async def menu_command_handler(message: types.Message):
	res, user = await auth(data=message)
	if not res: return;
	cfg = config.menu
	if await isAdmin(data=message):
		cfg[4]["Enable"] = True
	await bot.send_message(message.chat.id, text=config.lang[user["lang"]]["menu"], 
		reply_markup=menu_keyboard(config=cfg, index="0", lang=user["lang"], back=0))


# server async
bot.add_custom_filter(MenuCallbackFilter())
import asyncio
asyncio.run(bot.polling())




