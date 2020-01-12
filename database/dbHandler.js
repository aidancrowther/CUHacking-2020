const mongoClient = require('mongodb').MongoClient;
const fs = require('fs');

const url = "mongodb://localhost:27017/";

let filled = false;

function fill() {
    mongoClient.connect(url, (err, db)=> {
        if(err) {throw err;}
        let dbo = db.db("bf");
        dbo.createCollection("butterflies", (err,res)=>{
            if(err) {throw err;}
            console.log("Collection made");
        });
        let data = JSON.parse(fs.readFileSync('./database/data.JSON'));
        console.log(data);
        dbo.collection("butterflies").insertMany(data, (err, res) => {
            if(err) {throw err;}
            console.log("Added butterflies");
        });
        db.close();
    });
    filled = true;
}



exports.search = (val)=>{
    console.log("Running");
    let r = search(val);
    console.log("R is: ");
    console.log(r);
    return r;
}

exports.fill = ()=>{
    fill();
}