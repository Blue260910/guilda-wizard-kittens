const express = require("express");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");

const app = express();
const SEGREDO_JWT = "alohomora";

app.get("/feitiço", (req, res) => {
  res.type("text/plain").send(String(req.query.nome));
});

app.get("/senha", (req, res) => {
  const hash = crypto.createHash("md5").update(req.query.senha).digest("hex");
  res.send(hash);
});

app.get("/mapa", (req, res) => {
  const dados = jwt.decode(req.query.token);
  res.send(dados);
});

app.listen(3000);
