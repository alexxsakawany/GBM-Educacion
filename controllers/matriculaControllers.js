const express = require('express');
const router = express.Router();
const multer = require('multer');
const mysql = require('mysql2/promise');
require('dotenv').config();

const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function(req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});
const upload = multer({ storage: storage });


async function getConnection() {
  return await mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  });
}


router.post('/submit', upload.fields([
  { name: 'foto', maxCount: 1 },
  { name: 'identificacao', maxCount: 1 },
  { name: 'comprovativo', maxCount: 1 }
]), async (req, res) => {
  try {
    const {nome, nascimento, naturalidade, nacionalidade, encarregado, telefone, email,
      curso, classe, ensino
    } = req.body;

    const foto = req.files['foto'][0].filename;
    const identificacao = req.files['identificacao'][0].filename;
    const comprovativo = req.files['comprovativo'][0].filename;

    const conn = await getConnection();

    const sql = `INSERT INTO matriculas 
      (nome, nascimento, naturalidade, nacionalidade, encarregado, telefone, email, curso, classe, ensino, foto, identificacao, comprovativo)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    await conn.execute(sql, [nome, nascimento, naturalidade, nacionalidade, encarregado, telefone, email, curso, classe, ensino, foto, identificacao, comprovativo]);

    await conn.end();

    res.send('<h1>Inscrição recebida! Em análise.</h1><a href="/">Voltar</a>');
  } catch (error) {
    console.error(error);
    res.status(500).send('Erro ao processar inscrição.');
  }
});

module.exports = router;
