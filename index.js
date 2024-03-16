// import express from "express";
// import convert from './src/router/routerconvert.js'
const express = require("express");
require("dotenv").config();
const convert = require("./src/router/routerconvert.js");

const app = express();

const PORT = process.env.PORT || 8000;

// app.use(express.static());
app.use("/api/v1", convert);

app.listen(PORT, () => {
  console.log("connecting port ",PORT);
});
