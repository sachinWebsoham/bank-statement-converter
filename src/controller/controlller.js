const { spawnSync } = require('child_process');


   

const main = async (req,res) =>{

    const pythonScriptPath='python/extract_table_from_pdf.py'
    const args=[req.file.path]
       
    const pythonProcess=spawnSync('python',[pythonScriptPath,...args],{encoding:'utf-8'})
    const filePathOfExcel=pythonProcess.stdout.trim().split('\n')[0]
    if (filePathOfExcel.includes('Error')) {
        res.send({message:'Error while conversion'})
    }            
    // console.log("pythonprocess>>",pythonProcess.stdout.trim().split('\n')[0])  
    // console.log("pythonprocess>>",pythonProcess.stdout)
   
    // Check for errors      
// if (pythonProcess.error) {
//     console.error(`Error executing Python script: ${pythonProcess.error}`);
//     return;
// }  

// Log output from Python script
// console.log(`Output from Python script: ${pythonProcess.stdout}`);

// Log errors, if any
// if (pythonProcess.stderr) {
//     console.error(`Error from Python script: ${pythonProcess.stderr}`);
// }

// Process exit code
// console.log(`Python script exited with code ${pythonProcess.status}`);


    // let filePath = req.file.path;
    // console.log("req.file==>",req.file);
    // console.log("filePath==>",filePath);



    // call python script and pass the file path to the python script
    // let result = await pythonFnName(filePath);

    // perform result work

    // const file = pythonProcess; //file name
         res.download(filePathOfExcel ,(err)=>{
        if(err){
            console.error("error downloading file:",err);
            res.status(500).send("error downloading file")
        }
    })
    // res.send({msg:'ok'})
    
}

 const downloadfile = async (req,res)=>{
        const file = 'python/public/downloads/xlsx/1709619711827-indian.xlsx';
        
        
        res.download(file ,(err)=>{
            if(err){
                console.error("error downloading file:",err);
                res.status(500).send("error downloading file")
            }
        })
}


module.exports ={
    downloadfile,
    main
} 
    