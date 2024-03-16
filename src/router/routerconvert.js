

const express = require("express");
const  upload  = require ("../middleware/multer.js");
const {main,downloadfile} = require ("../controller/controlller.js")

const routes = express.Router()

routes.post('/convert',upload.single('pdfFile'),main)
routes.get('/download',downloadfile)

// export default routes; 
module.exports = routes 
