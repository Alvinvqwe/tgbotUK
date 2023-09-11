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

# database connection init
conn = connection()

# @decortator
def handle_exception(func):
	def wrapper(*args, **kw):
		try:
			return func(*args, **kw)
		except Exception as e:
			raise e
		finally:
			# conn.close()
			pass
	return wrapper

@handle_exception
def auth_(chat_id, isAdmin=0):
	sql = 'select * from employee where chatID="%s"'%(chat_id)
	if isAdmin:
		sql += " and isAdmin=1"
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()


@handle_exception
def lang_set(chat_id, lang):
	sql = 'update employee set lang="%s" where chatid="%s"'%(lang, chat_id)
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()

@handle_exception
def authByUsername(username):
	sql = 'select * from employee where username="%s"'%(username)
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()

@handle_exception
def user_update(chat_id, username=None, firstname=None, lastname=None, isRegister=False):
	p_ls = []
	sql = 'update employee set '
	sql_conditions = ""
	if firstname: p_ls.append('firstname=%s'%firstname)
	if lastname: p_ls.append('lastname=%s'%lastname)
	if isRegister:
		if not username:
			return -1
		p_ls.append('chatid="%s" '%chat_id)
		sql_conditions = ' where username="%s"'%username
	else:
		if username: p_ls.append('username=%s'%username)
		sql_conditions = ' where chatid="%s"'%chat_id

	if not p_ls:
		return 0
	sql = sql + " and ".join(p_ls) + sql_conditions
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()



