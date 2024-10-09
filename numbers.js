const express = require('express');
const cors = require('cors');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3000;
const helmet = require('helmet');

app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    next();
});

app.use(helmet());

app.use(cors({
    origin: 'https://rebuild-kc.com',  // 이 도메인만 허용
    methods: 'GET',  // GET 요청만 허용
    allowedHeaders: 'Content-Type'  // 허용된 헤더
}));

// form_data.json 파일을 클라이언트에게 제공
app.get('/data', (req, res) => {
    fs.readFile('form_data.json', 'utf-8', (err, data) => {
        if (err) {
            res.status(500).send('파일 읽기 오류');
        } else {
            res.json(JSON.parse(data));
        }
    });
});

app.listen(PORT, () => {
    console.log(`서버가 ${PORT}번 포트에서 실행 중입니다.`);
});
