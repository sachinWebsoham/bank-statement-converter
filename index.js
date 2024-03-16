// import express from "express";
// import convert from './src/router/routerconvert.js'
const express = require("express");
const convert = require('./src/router/routerconvert.js');

const app = express();

// app.use(express.static());
app.use('/api/v1',convert)














app.listen(8000, () => {
    console.log('Server is running on port 8000');
});




