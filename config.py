# tgbot host configurations
TELEBOT_BOT_TOKEN = "6000416074:AAGD_1u1UaVIgn43Ld0BsGv1IpZcUc99qy8"

TGBOT_NAME = "tgbotUK"

# database configurations
database = {
	"host": "217.146.82.143",
	"user": "admin",
	"password": "5pkYoco7YL5FVJ",
	"database": "tgbotUK",
	"charset": "utf8mb4"
}

chatID_ls = {
	"IT_support": "6063741839",
}

lang = {
	"cn": {
		"menu": "菜单",
		"auth_faild": "很抱歉，该机器人仅服务内部员工使用，如有疑问，请联系 Mario in London@Mariolondon",
		"lang_set_succeed": "设置语言成功",
		"auth_admin_faild": "很抱歉，您不是管理员，无法使用管理员功能，如有疑问，请联系 Mario in London@Mariolondon",
		"report_intro": "请使用 /makeAnReport_IT 命令 + 描述内容来反馈，相关工作人员会尽快联系您来解决该问题~",
		"empty_warn": "参数内容不合法，请按照格式输入",
		"sys_err": "系统内部错误，请联系 @Alvin_name 反馈.",
		"post_intro": "请使用 /makeAnPost 命令 + 发布内容",
		"task_done": "已完成",
		"add_user": "请使用 /add_user 命令 + 员工ID:TG的username:部门ID 格式来添加新员工，添加后请新员工关注 @xxx",
		"department_ls": '''部门列表如下: (部门ID, 部门名称)
'1','市场部'
'2','后勤部'
'3','行政部'
'4','财务部'
'5','审计部'
'6','人事部'
'7','赢创项目组'
'8','德星项目组'
'9','嘉华项目组'
'10','天宇项目组'
'11','Venus(Spring)'
'12','Mirror' ''',
		"remove_user": "请使用 /remove_user + employeeID 命令来删除员工",
		"update_user": "请使用 /update_user + username, employeeID:new_employeeID, departmentID:new_departmentID ... 格式来更新员工信息",
		"check_user": "用户不存在, 请检查输入",
		"params_err": "参数错误, 请重新输入"
	},
	"en": {
		"menu": "menu",
		"auth_faild": "Sorry, this bot service to employees only, if any questions, please contact to Mario in London@Mariolondon",
		"lang_set_succeed": "Set the languange successful",
		"auth_admin_faild": "Sorry, you are not administrator, if any questions, please contact to Mario in London@Mariolondon",
		"report_intro": "please use command: /makeAnReport_IT + the issues description to report，we will sort it as fast as we can~",
		"empty_warn": "the issues description is not valid, please input by following format",
		"sys_err": "system error, please contact @Alvin_name to report.",
		"post_intro": "Please use command: /makeAnPost + the post content",
		"task_done": "task done",
		"add_user": "Please use command /add_user + employeeID:username:departmentID format to add new，then after added, please alert the new to follow @xxx",
		"department_ls": "",
		"remove_user": "Please use command /remove_user + employeeID format to remove",
		"update_user": "Please use command /update_user + employeeID:new_employeeID, departmentID:new_departmentID ... format to update",
		"check_user": "user is not exist, please check the input",
		"params_err": "params not valid, please re-input by the format"
	}
}


menu = [
	{
		"display": {
			"en": "clock in/out",
			"cn": "签到/签退"
			}, 
		"id": "0",
		"submenu": [
			{
				"display": {
					"en": "clock",
					"cn": "打卡"
					}, 
				"id": "00",
				"submenu": [],
				"link": "https://www.youtube.com/watch?v=EDH6DsoKs1I",
				"Enable": True
			},
			{
				"display": {
					"en": "history", 
					"cn": "打卡历史"
					},
				"id": "01", 
				"submenu": [
					{
						"display": {
							"en": "daily",
							"cn": "本日"
							},
						"id": "011", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "monthly",
							"cn": "本月"
							},
						"id": "012", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
				],
				"link": "",
				"Enable": True
			}

		],
		"Enable": True
	},
	{
		"display": {
			"en": "posts", 
			"cn": "公告"
			}, 
		"id": "1",
		"submenu": [
			{
				"display": {
					"en": "the latest post", 
					"cn": "最新一条"
					}, 
				"id": "10",
				"submenu": [],
				"link": "",
				"Enable": True
			},
			{
				"display": {
					"en": "history", 
					"cn": "历史公告"
					}, 
				"id": "11",
				"submenu": [],
				"link": "",
				"Enable": True
			},
		],
		"Enable": True
	},
	{
		"display": {
			"en": "report",
			"cn": "问题举报/反馈"
			},
		"id": "2", 
		"submenu": [
			{
				"display": {
					"en": "IT issues", 
					"cn": "IT 问题反馈"
					},
				"id": "20", 
				"submenu": [],
				"link": "",
				"Enable": True
			},
			{
				"display": {
					"en": "office issues", 
					"cn": "职场问题反馈"
					}, 
				"id": "21",
				"submenu": [],
				"link": "",
				"Enable": False
			},
			{
				"display": {
					"en": "report history", 
					"cn":"举报历史"
					}, 
				"id": "22",
				"submenu": [],
				"link": "",
				"Enable": True
			},
		],
		"Enable": True
	},
	{
		"display": {
			"en": "settings", 
			"cn": "设置"
			}, 
		"id": "3",
		"submenu": [
			{
				"display": {
					"en": "language setting", 
					"cn":"语言设置"
					}, 
				"id": "30",
				"submenu": [
					{
						"display": {
							"en": "Chinese",
							"cn": "中文"
							},
						"id": "300", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "English",
							"cn": "英文"
							},
						"id": "301", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
				],
				"link": "",
				"Enable": True
			},
		],
		"Enable": True
	},
	{
		"display": {
			"en": "admin menu", 
			"cn": "管理员菜单"
			}, 
		"id": "4",
		"submenu": [
			{
				"display": {
					"en": "reports management",
					"cn": "举报管理"
					},
				"id": "40", 
				"submenu": [],
				"link": "",
				"Enable": True
			},
			{
				"display": {
					"en": "clocks management",
					"cn": "打卡管理"
					},
				"id": "41", 
				"submenu": [
					{
						"display": {
							"en": "monthly history",
							"cn": "本月记录"
							},
						"id": "410", 
						"submenu": [
							{
								"display": {
									"en": "by department",
									"cn": "按部门查询"
									},
								"id": "4100", 
								"submenu": [
									{
										"display": {
											"en": "行政部",
											"cn": "行政部"
											},
										"id": "41000", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "财务部",
											"cn": "财务部"
											},
										"id": "41001", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "审计部",
											"cn": "审计部"
											},
										"id": "41002", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "人事部",
											"cn": "人事部"
											},
										"id": "41003", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "赢创项目组",
											"cn": "赢创项目组"
											},
										"id": "41004", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "德星项目组",
											"cn": "德星项目组"
											},
										"id": "41005", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "嘉华项目组",
											"cn": "嘉华项目组"
											},
										"id": "41006", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "天宇项目组",
											"cn": "天宇项目组"
											},
										"id": "41007", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "Venus(Spring)",
											"cn": "Venus(Spring)"
											},
										"id": "41008", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "Mirror",
											"cn": "Mirror"
											},
										"id": "41009", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
								],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "all departments",
									"cn": "所有查询"
									},
								"id": "4101", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
						],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "daily history",
							"cn": "本日记录"
							},
						"id": "411", 
						"submenu": [
							{
								"display": {
									"en": "by department",
									"cn": "按部门查询"
									},
								"id": "4110", 
								"submenu": [
									{
										"display": {
											"en": "行政部",
											"cn": "行政部"
											},
										"id": "41100", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "财务部",
											"cn": "财务部"
											},
										"id": "41101", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "审计部",
											"cn": "审计部"
											},
										"id": "41102", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "人事部",
											"cn": "人事部"
											},
										"id": "41103", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "赢创项目组",
											"cn": "赢创项目组"
											},
										"id": "41104", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "德星项目组",
											"cn": "德星项目组"
											},
										"id": "41105", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "嘉华项目组",
											"cn": "嘉华项目组"
											},
										"id": "41106", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "天宇项目组",
											"cn": "天宇项目组"
											},
										"id": "41107", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "Venus(Spring)",
											"cn": "Venus(Spring)"
											},
										"id": "41108", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
									{
										"display": {
											"en": "Mirror",
											"cn": "Mirror"
											},
										"id": "41109", 
										"submenu": [],
										"link": "",
										"Enable": True
									},
								],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "all departments",
									"cn": "所有查询"
									},
								"id": "4111", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
						],
						"link": "",
						"Enable": True
					},
				],
				"link": "",
				"Enable": True
			},
			{
				"display": {
					"en": "posts management", 
					"cn": "公告管理"
					}, 
				"id": "42",
				"submenu": [
					{
						"display": {
							"en": "make a post",
							"cn": "发布新公告"
							},
						"id": "420", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "check the posts list",
							"cn": "查看发布历史"
							},
						"id": "421", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
				],
				"link": "",
				"Enable": True
			},
			{
				"display": {
					"en": "employees management", 
					"cn": "员工管理"
					}, 
				"id": "43",
				"submenu": [
					{
						"display": {
							"en": "add",
							"cn": "添加员工"
							},
						"id": "430", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "remove",
							"cn": "删除员工"
							},
						"id": "431", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "update",
							"cn": "更改员工信息"
							},
						"id": "432", 
						"submenu": [],
						"link": "",
						"Enable": True
					},
					{
						"display": {
							"en": "check the list",
							"cn": "查看员工列表"
							},
						"id": "433", 
						"submenu": [
							{
								"display": {
									"en": "all",
									"cn": "所有部门"
									},
								"id": "4330", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "行政部",
									"cn": "行政部"
									},
								"id": "4331", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "财务部",
									"cn": "财务部"
									},
								"id": "4332", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "审计部",
									"cn": "审计部"
									},
								"id": "4333", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "人事部",
									"cn": "人事部"
									},
								"id": "4334", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "赢创项目组",
									"cn": "赢创项目组"
									},
								"id": "4335", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "德星项目组",
									"cn": "德星项目组"
									},
								"id": "4336", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "嘉华项目组",
									"cn": "嘉华项目组"
									},
								"id": "4337", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "天宇项目组",
									"cn": "天宇项目组"
									},
								"id": "4338", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "Venus(Spring)",
									"cn": "Venus(Spring)"
									},
								"id": "4339", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
							{
								"display": {
									"en": "Mirror",
									"cn": "Mirror"
									},
								"id": "433x", 
								"submenu": [],
								"link": "",
								"Enable": True
							},
						],
						"link": "",
						"Enable": True
					},
				],
				"link": "",
				"Enable": True
			},
		],
		"Enable": False
	},	
]

