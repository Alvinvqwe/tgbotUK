from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import types
import model
import config

class employeeStates(StatesGroup):
	# statesgroup should contain states
    user_info = State()
    # chat_id = State()
    # username = State()

# tg bot init
bot = AsyncTeleBot(config.TELEBOT_BOT_TOKEN, state_storage=StateMemoryStorage())

# authorication
def auth(data):
	# check chatid
	chat_id = data.from_user.id
	res, user_ = model.auth_(chat_id)
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
			return True, user_[0]
		else:
			# users if not valid
			bot.send_message(chat_id, text=config.lang["en"]["auth_faild"])
			return None, None
	else:
		# check if username and firstname/lastname have been updated
		# print(data.from_user)
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
def isAdmin(data):
	# check chatid
	chat_id = data.from_user.id
	res, user_ = model.auth_(chat_id, isAdmin=1)
	if not res:
		bot.send_message(chat_id, text=config.lang[user_[0]["lang"]]["auth_admin_faild"])
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
	res_, user = auth(data=call)
	if not res_: 
		await bot.send_message(call.message.chat.id, text=config.lang[dics[message.text]]["lang_set_succeed"])
		return;
	# isAdmin = isAdmin(data=call)
	callback_data: dict = func_menu.parse(callback_data=call.data)

	menu_id = int(callback_data['menu_id'])
	res = callback_data['menu_id']
	lang = user["lang"]

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

	# clock
	elif res in ["00"]:
		web_app = types.WebAppInfo(url='https://127.0.0.1:3000?'+"chatid="+str(call.message.chat.id))
		button_c_in = types.InlineKeyboardButton('clock', web_app=web_app)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(button_c_in)
		await bot.send_message(call.message.chat.id, text='clock', reply_markup=keyboard)

	# posts
	elif res in ["10", "11"]:
		# 10 latest
		# 11 history
		pass

	# 问题举报
	elif res in ["20", "22"]:
		pass

	################
	# admin section
	################
	elif res in ["40", "41", "42", "43"]:
		pass

	else:
		# direct to the section configs
		title, cfg = render_menu(callback_data['menu_id'], action=1, lang_set=lang, isAdmin=isAdmin(data=call))
		back = 0 if title in [config.lang["cn"]["menu"], config.lang["en"]["menu"]] else 1
		keyboard = menu_keyboard(config=cfg, index=res, lang=lang, back=back, action=1)
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
				text=title, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
async def menu_command_handler(message):
	res_, user = auth(data=message)
	if not res_: return;

	res = message.data
	# print(res)
	lang = user["lang"]
	index = res.split("_")[-1]
	# get the section configs
	title, cfg = render_menu(index, action=0, lang_set=lang, isAdmin=isAdmin)
	# print(cfg)
	back = 0 if title in [config.lang["cn"]["menu"], config.lang["en"]["menu"]] else 1
	keyboard = menu_keyboard(config=cfg, index=index, lang=user["lang"], back=back, action=0)
	await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
						text=title, reply_markup=keyboard)


# lang set callback
@bot.message_handler(content_types=["text"], func=lambda message: message.text in ["English", "中文"])
async def lang_set(message):
	res, user = auth(data=message)
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
	if isAdmin(data=message):
		cfg[4]["Enable"] = True
	await bot.send_message(message.chat.id, text=config.lang[dics[message.text]]["menu"], 
		reply_markup=menu_keyboard(config=cfg, index="0", lang=dics[message.text], back=0, action=1))


########################## 
# commands list
@bot.message_handler(commands=['start'])
async def greeting(message):
	res, user = auth(data=message)
	if not res: return;
	chat_id = message.from_user.id
	keyboard = lang_set_keyboard()
	sent_msg = await bot.send_message(chat_id, text='please select a language', reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
async def menu_command_handler(message: types.Message):
	res, user = auth(data=message)
	if not res: return;
	cfg = config.menu
	if isAdmin(data=message):
		cfg[4]["Enable"] = True
	await bot.send_message(message.chat.id, text=config.lang[user["lang"]]["menu"], 
		reply_markup=menu_keyboard(config=cfg, index="0", lang=user["lang"], back=0))


# 打卡功能
# 调动 webapp
# nodejs -> mysql 打卡写入
# 1 hrs




# 打卡查询功能
# 1 hrs


@bot.message_handler(commands=['clock_in'])
async def send_id(message):
    web_app = types.WebAppInfo(url='https://www.youtube.com/watch?v=EDH6DsoKs1I')
    button_c_in = types.InlineKeyboardButton('clock in', web_app=web_app)
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_c_in)
    await bot.send_message(chat_id, text='please clock in through the link', reply_markup=keyboard)






# server async
bot.add_custom_filter(MenuCallbackFilter())
import asyncio
asyncio.run(bot.polling())




