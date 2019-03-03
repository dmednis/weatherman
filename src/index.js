const Koa = require('koa');
const ip = require('ip');
const bodyParser = require('koa-bodyparser');
const config = require('config');
const knex = require('knex');

const dbConfig = config.get('db');
const db = knex(dbConfig);

const app = new Koa();
app.use(bodyParser());


function insertReading(sensor, value) {
    db('readings').insert({sensor, value})
        .returning('*')
        .then(() => console.log("inserted"));
}

app.use(async ctx => {
    const {url, method, body} = ctx.request;
    console.log(url);
    console.log(method);
    console.log(body);
    const {value, sensor} = body;
    if (value && sensor) {
        insertReading(sensor, value);
    }
    ctx.body = 'Hello World';
});

app.listen(3000);
console.log("LISTENING ON 3000");
console.log(ip.address());