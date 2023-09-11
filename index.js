const fs = require('fs');
const Koa = require('koa');
const https = require('https');
const app = new Koa();

// 读取 SSL/TLS 证书和私钥文件
const privateKey = fs.readFileSync('private-key.pem', 'utf8');
const certificate = fs.readFileSync('certificate.pem', 'utf8');

// 创建 HTTPS 服务器
const credentials = { key: privateKey, cert: certificate };
const httpsServer = https.createServer(credentials, app.callback());

var mysql = require('mysql');
var connection = mysql.createConnection({
    host: '217.146.82.143',
    user: 'admin',
    password: '5pkYoco7YL5FVJ',
    database: 'tgbotUK'
});


// 217.146.82.143
// localhost
connection.connect();

const datetime = require("silly-datetime")

// 获取用户 chatid
app.use(async ctx => {
    const headers = ctx.headers;
    var ips_ = "None"
    if (headers['x-real-ip']) {
        ips_ = headers['x-real-ip'];
    }
    if (headers['x-forwarded-for']) {
        const ipList = headers['x-forwarded-for'].split(',');
        ips_ = ipList[0];
    }


    if ("chatid" in ctx.query) {
        res = {
            "employeeID": "",
            "ip": "",
            "time": ""
        }
        IPls = []

        // 查询用户 id 是否存在
        await connection.query('SELECT * FROM tgbotUK.employee where chatID=' + ctx.query["chatid"],
        function(error, results, fields) {
            if (error) {
                ctx.body = "UserID not valied 身份验证失败"
                return;
                // throw error
            };
            console.log(results[0])
            res["employeeID"] = results[0].idemployee
        });

        // 获取 IP 列表
        await connection.query('SELECT IPs FROM tgbotUK.office',
        function(error, results, fields) {
            if (error) throw error;
            // console.log(results)
            results.forEach(e => {
                if (e["IPs"]) {
                    ls = e["IPs"].split(",") 
                    ls.forEach(i => {
                        IPls.push(i)
                    })
                }
            });
            // console.log("IP list: ", IPls);
            console.log(ctx.ip)
            if (ctx.ip in IPls) {
                res["ip"] = ctx.ip
            } else {
                ctx.body = "IP not valied IP验证失败";
                console.log(ctx.body);
                return ctx.body;
            }
        });
        // 获取当前时间
        const time = datetime.format(new Date(), "YYYY-MM-DD HH:mm")
        res["time"] = time

        // 查询，今日打卡记录
        await connection.query('SELECT * FROM tgbotUK.clocks where employeeID=' + res["employeeID"] + " and TO_DAYS(order_time) = TO_DAYS(NOW())",
        function(error, results, fields) {
            console.log("3:", res)
            if (error) throw error;
            if (results.clockin) {
                // 写入 clock out
                var addSql = 'INSERT INTO clocks(employeeID,IP,clockin,clockout) VALUES(?,?,?,?)';
            } else {
                // 写入 clock in
                var addSql = 'INSERT INTO clocks(employeeID,IP,clockin,clockout) VALUES(?,?,?,?)';
            }
            connection.query(addSql, addSqlParams,
            function(err, result) {
                if (err) {
                    console.log('[INSERT ERROR] - ', err.message);
                    return;
                }
                console.log('INSERT ID:', result);
            });
            // 返回打卡成功
            ctx.body = "打卡成功!"
        });
    } else {
        // 返回用户 id 错误
        ctx.body = "UserID not valied 身份验证失败"
    }

    // 获取参数，chatid ✅
    // 查询用户 id 是否存在，不存在则返回用户 id 错误 ✅
    // 查询用户 ip 是否正确, 不存在则返回 IP 错误, 请到办公室连接 wifi 打卡
    // 获取当前时间
    // 查询，写入打卡记录
    // 返回打卡成功
    // ctx.body = JSON.stringify(ctx.headers);
    // ctx.body = {"ip": ctx.ip, "chatid": ctx.query["chatid"]};
});


// 启动 HTTPS 服务器
const port = 443; // HTTPS 默认端口
httpsServer.listen(port, () => {
  console.log(`HTTPS server is running on port ${port}`);
});
