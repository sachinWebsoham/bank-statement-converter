// import multer from "multer";
const multer = require ("multer");


// const multer = require('multer');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/pdf');
        // cb(null, 'python');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname); 
    }
});

// export const upload = multer({ storage: storage });
module.exports = multer({ storage: storage });












// const Storage = multer.diskStorage({
//   destination:'public/files',
//   filename:(req,file,callback) =>{
//       const ext = file.mimetype.split("/")[1];
//       callback(null, `${file.fieldname}_${Date.now()}.${ext}`);
//   }
// })
// export const upload = multer({
//   storage:Storage
// });