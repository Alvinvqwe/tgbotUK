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


# users
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


@handle_exception
def user_add(idemployee, username, firstname, departmentID=0, chatid=None, lastname=None, isAdmin=0, lang="en"):
	if not idemployee or not username:
		return -1
	sql = f'INSERT INTO tgbotUK.employee (idemployee, chatid, username, departmentID, firstname, lastname, isAdmin, lang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'%(idemployee, chatid, username, departmentID, firstname, lastname, isAdmin, lang)
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()
	return 1


@handle_exception
def remove(idemployee):
	if not idemployee: return -1
	sql = f'DELETE FROM tgbotUK.employee WHERE idemployee="%s"'%idemployee
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()
	return 1

@handle_exception
def user_list(department_id=-1):
	sql = f'SELECT * FROM tgbotUK.employee'
	if department_id:
		sql = f'SELECT * FROM tgbotUK.employee where department_id=%s'%department_id
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()

@handle_exception
def department_list(department_id=-1):
	sql = f'SELECT * FROM tgbotUK.department'
	if department_id:
		sql = f'SELECT * FROM tgbotUK.department where department_id=%s'%department_id
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()

# post
@handle_exception
def add_post(ctx, date, publisher_chatid, type_=0, attaches=None):
	if not ctx or not date or not publisher_chatid: return -1
	sql = f'INSERT INTO tgbotUK.posts (content, type, date, attaches, publisher_chatid) VALUES (%s, %s, %s, %s, %s)'%(ctx, type_, date, attaches, publisher_chatid)
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()
	return 1

@handle_exception
def posts_list(num=0):
	sql = f'SELECT * FROM tgbotUK.posts'
	if num:
		sql = f'SELECT * FROM tgbotUK.posts ORDER BY timestamp DESC LIMIT %s'%num
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()

# clocks
@handle_exception
def clock_check(idemployee, range_="day"):
	if not idemployee: return -1
	sql = f'SELECT * FROM tgbotUK.clocks where employeeID=%s and TO_DAYS(clockin) = TO_DAYS(NOW())'%idemployee
	if range_ == "month":
		sql = f'SELECT * FROM tgbotUK.clocks where employeeID=%s and DATE_FORMAT(clockin, "%Y%m")=DATE_FORMAT(CURDATE(), "%Y%m")'%idemployee
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()

@handle_exception
def clocks_report(department_id=0, range_="day"):
	sql = ""
	if not department_id:
		sql = f'''SELECT c.employeeID, c.clockin, c.clockout, e.username, o.officeName
					FROM tgbotUK.clocks c 
					LEFT JOIN tgbotUK.employee e ON e.idemployee = c.employeeID 
					LEFT JOIN tgbotUK.office o ON o.IPs LIKE CONCAT('%', c.IP, '%')
					WHERE TO_DAYS(c.clockin) = TO_DAYS(NOW());'''
		if range_ == "month":
			sql = f'''SELECT c.employeeID, c.clockin, c.clockout, e.username, o.officeName
					FROM tgbotUK.clocks c 
					LEFT JOIN tgbotUK.employee e ON e.idemployee = c.employeeID 
					LEFT JOIN tgbotUK.office o ON o.IPs LIKE CONCAT('%', c.IP, '%')
					WHERE DATE_FORMAT(clockin, "%Y%m")=DATE_FORMAT(CURDATE(), "%Y%m");'''
	else:
		sql = f'''SELECT c.employeeID, c.clockin, c.clockout, e.username, o.officeName
			FROM tgbotUK.clocks c 
			LEFT JOIN tgbotUK.employee e ON e.idemployee = c.employeeID 
			LEFT JOIN tgbotUK.office o ON o.IPs LIKE CONCAT('%', c.IP, '%')
			WHERE e.departmentID=%s and TO_DAYS(c.clockin) = TO_DAYS(NOW());'''%department_id
		if range_ == "month":
			sql == f'''SELECT c.employeeID, c.clockin, c.clockout, e.username, o.officeName
					FROM tgbotUK.clocks c 
					LEFT JOIN tgbotUK.employee e ON e.idemployee = c.employeeID 
					LEFT JOIN tgbotUK.office o ON o.IPs LIKE CONCAT('%', c.IP, '%')
					WHERE e.departmentID=%s and DATE_FORMAT(clockin, "%Y%m")=DATE_FORMAT(CURDATE(), "%Y%m");'''%department_id
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()


@handle_exception
def report_list(idemployee=None):
	sql = f"SELECT * FROM tgbotUK.report"
	if idemployee:
		sql = f"SELECT * FROM tgbotUK.report where r_employeeID=%s"%idemployee
	with conn.cursor() as cursor:
		return cursor.execute(sql), cursor.fetchall()


# type: 0:IT, 1:other
@handle_exception
def make_report(idemployee, content, date, type_=0):
	if not idemployee: return -1;
	sql = f'INSERT INTO tgbotUK.report (r_employeeID, type, content, attaches, date) VALUES (%s, %s, %s, %s, %s)'%(idemployee, type_, content, None, date)
	with conn.cursor() as cursor:
		cursor.execute(sql)
	conn.commit()
	return 1









