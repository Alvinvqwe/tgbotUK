const fs = require('fs');
const Koa = require('koa');
const https = require('https');
const mysql = require('mysql2/promise'); // 使用 mysql2/promise 模块
const datetime = require("silly-datetime");
//const ip = require('koa-ip');
const app = new Koa();

// 创建 HTTPS 服务器
const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};
const httpsServer = https.createServer(options, app.callback());

// 创建 MySQL 连接池
const pool = mysql.createPool({
  host: '217.146.82.143',
  user: 'admin',
  password: '5pkYoco7YL5FVJ',
  database: 'tgbotUK'
});

//app.use(ip());


function getClientIP(req) {
  let ip= req.headers['x-forwarded-for'] ||     // 判断是否有反向代理 IP
    req.ip  ||
    req.connection.remoteAddress ||             // 判断 connection 的远程 IP
    req.socket.remoteAddress ||                 // 判断后端的 socket 的 IP
    req.connection.socket.remoteAddress || ''
  if(ip) {
    ip = ip.replace('::ffff:', '')
  }
  return ip;
}


app.use(async (ctx) => {
  //const headers = ctx.headers;
  //console.log(ctx.request.ip)
  //const ips = headers['x-real-ip'] || (headers['x-forwarded-for'] && headers['x-forwarded-for'].split(',')[0]) || 'None';
  //console.log(headers['x-real-ip'], headers['x-forwarded-for'])
  ip = getClientIP(ctx)
  console.log(ip)
  if ("chatid" in ctx.query) {
    try {
      const connection = await pool.getConnection();
      const [employeeRows] = await connection.query('SELECT * FROM tgbotUK.employee WHERE chatID = ?', [ctx.query["chatid"]]);
      //console.log(employeeRows)
      if (employeeRows.length === 0) {
        ctx.body = "UserID not valid 身份验证失败";
      } else {
        const res = {
          "employeeID": employeeRows[0].idemployee,
          "ip": "",
          "time": ""
        };
        
        const [officeRows] = await connection.query('SELECT IPs FROM tgbotUK.office');
        const IPls = [];
        officeRows.forEach((e) => {
          if (e["IPs"]) {
            const ipsList = e["IPs"].split(",");
            ipsList.forEach(i => {
              IPls.push(i);
            });
          }
        });

        //const res_ip = ips.substr(7, 15); // 处理获取的 IP
    //console.log(ips, res_ip, IPls)
        if (IPls.includes(ip)) {
          res["ip"] = ip;
        } else {
          ctx.body = "IP not valid IP验证失败";
          connection.release();
          return;
        }

        const time = datetime.format(new Date(), "YYYY-MM-DD HH:mm");
        res["time"] = time;

        const [clockRows] = await connection.query('SELECT * FROM tgbotUK.clocks WHERE employeeID = ? AND TO_DAYS(clockin) = TO_DAYS(NOW())', [res["employeeID"]]);

        if (clockRows.length === 0) {
          // 写入 clock in
          const addSql = 'INSERT INTO clocks(employeeID, IP, clockin, clockout) VALUES (?, ?, ?, ?)';
          await connection.query(addSql, [res["employeeID"], res["ip"], time, null]);
        } else {
          // 写入 clock out
          const addSql = 'UPDATE clocks SET clockout = ? WHERE idclocks = ?';
          //console.log(clockRows[0], clockRows[0].idclocks)
          await connection.query(addSql, [time, clockRows[0].idclocks]);
        }

        connection.release();
        ctx.body = "打卡成功!";
      }
    } catch (error) {
      console.error('Error:', error);
      ctx.body = "Internal Server Error";
    }
  } else {
    ctx.body = "UserID not valid 身份验证失败";
  }
});

// 启动 HTTPS 服务器
const port = 443; // HTTPS 默认端口
httpsServer.listen(port, () => {
  console.log(`HTTPS server is running on port ${port}`);
});