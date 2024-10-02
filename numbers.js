const express = require('express');
const cors = require('cors');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`서버가 ${port}번 포트에서 실행 중입니다.`);
});

app.use(cors({
    origin: '*',  // 모든 출처를 허용하거나 특정 출처만 허용할 수 있습니다.
    methods: ['GET', 'POST'],
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

app.listen(3000, () => {
    console.log('서버가 3000번 포트에서 실행 중입니다.');
});
