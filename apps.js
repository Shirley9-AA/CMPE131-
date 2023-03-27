const express = require('express');
const app = express();
const session = require('express-session');
const bodyParser = require('body-parser');

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true
}));



app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});
