const sd = require('silly-datetime');

// 获取当前时间
const now = new Date();

// 设置目标时区
const targetTimezone = 'Europe/London'; // 例如，纽约时区

// 转换为目标时区的时间
const targetDatetime = now.toLocaleString('en-US', { timeZone: targetTimezone });

// 使用 silly-datetime 格式化时间
const formattedTime = sd.format(targetDatetime, 'YYYY-MM-DD HH:mm:ss');

console.log('Formatted time in the target timezone:', formattedTime);
