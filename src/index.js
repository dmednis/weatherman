const Koa = require('koa');
const ip = require('ip');
const bodyParser = require('koa-bodyparser');
const config = require('config');
const knex = require('knex');

const dbConfig = config.get('db');
const db = knex(dbConfig);

const app = new Koa();
app.use(bodyParser());


function insertReading(value) {
    db('readings').insert({value})
        .returning('*')
        .then(() => console.log("inserted"));
}

app.use(async ctx => {
    console.log(ctx.request.url);
    console.log(ctx.request.method);
    console.log(ctx.request.body);
    if (ctx.request.body.value) {
        insertReading(ctx.request.body.value);
    }
    ctx.body = 'Hello World';
});

app.listen(3000);
console.log("LISTENING ON 3000");
console.log(ip.address());