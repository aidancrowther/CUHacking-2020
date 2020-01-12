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
        let data = JSON.parse(fs.readFileSync('./data.JSON'));
        dbo.collection("butterflies").insertMany(data, (err, res) => {
            if(err) {throw err;}
            console.log("Added butterflies");
        });
        db.close();
    });
    filled = true;
}

function search(val) {
    if(!filled) {
        fill();
    }

    mongoClient.connect(url, (err, db) => {
        if(err) {throw err;}

        let dbo = db.db("butterflies")
        let query = {"name" : val};
        dbo.find(query).toArray((err, result)=>{
            if(err) {throw err;}
            db.close();
            return result;
        });
    });
}