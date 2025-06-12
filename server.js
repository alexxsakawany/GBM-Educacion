require('dotenv').config();
const express = require('express');
const mysql = require('mysql2');
const multer = require('multer');
const path = require('path');
const app = express();

// Config multer (pasta uploads)
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});
const upload = multer({ storage });

// Conexão com MySQL
const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

// Middleware para pegar os dados do form
app.use(express.urlencoded({ extended: true }));

// Serve o form.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'form.html'));
});

// Rota POST para receber o form com arquivos
app.post('/submit', upload.fields([
  { name: 'foto', maxCount: 1 },
  { name: 'identificacao', maxCount: 1 },
  { name: 'comprovativo', maxCount: 1 }
]), (req, res) => {
  const dados = req.body;
  const foto = req.files['foto'][0].filename;
  const identificacao = req.files['identificacao'][0].filename;
  const comprovativo = req.files['comprovativo'][0].filename;

  const sql = `
    INSERT INTO matriculas 
    (nome, nascimento, naturalidade, nacionalidade, encarregado, telefone, email, curso, classe, ensino, foto, identificacao, comprovativo) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;const values = [
    dados.nome,
    dados.nascimento,
    dados.naturalidade,
    dados.nacionalidade,
    dados.encarregado,
    dados.telefone,
    dados.email,
    dados.curso,
    dados.classe,
    dados.ensino,
    foto,
    identificacao,
    comprovativo
  ];

  connection.query(sql, values, (err) => {
    if (err) {
      console.error('Erro ao salvar no banco:', err);
      return res.status(500).send('Erro interno');
    }
    res.redirect('/sucesso.html');
  });
});
// Serve a página de sucesso
app.get('/sucesso.html', (req, res) => {
  res.send('<h1>Matricula enviada com sucesso! Em análise.</h1>');
});

// Iniciar servidor
app.listen(3000, () => console.log('Servidor rodando na porta 3000'));



