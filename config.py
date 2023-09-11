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


lang = {
	"cn": {
		"menu": "菜单",
		"auth_faild": "很抱歉，该机器人仅服务内部员工使用，如有疑问，请联系 Mario in London@Mariolondon",
		"lang_set_succeed": "设置语言成功",
		"auth_admin_faild": "很抱歉，您不是管理员，无法使用管理员功能，如有疑问，请联系 Mario in London@Mariolondon"
	},
	"en": {
		"menu": "menu",
		"auth_faild": "Sorry, this bot service to employees only, if any questions, please contact to Mario in London@Mariolondon",
		"lang_set_succeed": "Set the languange successful",
		"auth_admin_faild": "Sorry, you are not administrator, if any questions, please contact to Mario in London@Mariolondon",
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
				"id": "02", 
				"submenu": [],
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
				"submenu": [],
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
									"en": "department list",
									"cn": "请选择部门"
									},
								"id": "4330", 
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

