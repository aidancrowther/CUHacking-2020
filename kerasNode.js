const tf = require("@tensorflow/tfjs");
const tfn = require("@tensorflow/tfjs-node");
const handler = tfn.io.fileSystem("./keras_model/model.json");
const express = require('express');
const wikijs = require('wikipediajs');
var bodyParser = require('body-parser');
let multer = require('multer');
const db = require("./database/dbHandler.js");
const crypto = require('crypto');
const mime = require('mime');
const mongoClient = require('mongodb').MongoClient;
const PNG = require('pngjs').PNG;
const fs = require('fs')
const getPixels = require('get-pixels');

const url = "mongodb://localhost:27017/";

var app = express();

let Storage = multer.diskStorage({
	destination: function(req, file, callback){
		callback(null, './temp/');
	},
	filename: function(req, file, callback){
		crypto.pseudoRandomBytes(16, function (err, raw) {
			callback(null, raw.toString('hex') + Date.now() + '.' + mime.extension(file.mimetype));
		});
	}
});

let upload = multer({
	storage: Storage
});


// We'll see if we need a database
//const MongoClient = require('mongodb').MongoClient;

// Just a dictionary for all the butterflies
const butterflies ={0 : "epargyreus_clarus", 1 : "limenitis_archippus", 2 : "caligo_memnon", 3 : "ornithoptera_priamus", 4 : "kallima_inachus", 
                    5 : "heliconius_ismenius", 6 : "heliconius_cydno", 7 : "danaus_plexippus", 8: "heliconius_hortense", 9: "biblis_hyperia",
                    10 : "euploea_modesta", 11 : "graphium_agamemnon", 12 : "athyma_perius", 13 : "heliconius_hecale", 14 : "siproeta_epaphus",
                    15 : "junonia_lemonias", 16 : "heliconius_charithonia", 17 : "parthenos_sylvia", 18 : "caligo_eurilochus", 19 : "papilio_palinurus", 
                    20 : "cethosia_cyane", 21 : "heliconius_erato", 22 : "nymphalis_vaualbum", 23 : "papilio_thoas", 24 : "papilio_cresphontes", 25 : "papilio_polyxenes",
                    26 : "parthenos_sylvia_brown", 27 : "boloria_selene", 28 : "agraulis_vanillae", 29 : "limenitis_arthemis", 30 : "hamadryas_amphinome",
                    31 : "heliconius_doris", 32 : "junonia_coenia", 33 : "morpho_peleides", 34 : "colias_interior", 35 : "satyrium_liparops", 36 : "phyciodes_tharos",
                    37 : "lycaena_phlaeas", 38 : "nymphalis_milberti", 39 : "troides_helena", 40 : "colobura_dirce", 41 : "morpho_polyphemus", 42 : "papilio_dardanus",
                    43 : "danaus_chrysippus", 44 : "dryas_iulia", 45 : "dryadula_phaetusa", 46 : "idea_leuconoe", 47 : "anartia_jatrophae"};

//server constants
const ROOT = './interface';
const PORT = 4000;

let model;
var retur;

callMe();

var urlEncodedParser = bodyParser.urlencoded({ extended: true });
app.use(express.static('interface'));
app.use(function(err, req, res, next) {
	console.log('Invalid field: ', err.field);
	next(err);
})

//respond to request for index.html
app.get('/', function(req, res){
  res.sendFile( ROOT + '/index.html');
});

app.post('/getResult', urlEncodedParser, function(req, res){
  //db.fill();
  /*
  let image = req.body['image'].map(Number);
  let imgTensor = tf.tensor(image, [1, 400, 400, 3]);
  let pred = butterflies[model.predict(imgTensor).dataSync()];
  */

  // Just a lil testy bit
  let butter = butterflies[40];

  mongoClient.connect(url, (err, db) => {
    if(err) {throw err;}

    let dbo = db.db("bf")
    let query = {"lname" : butter};

    console.log("Querying");
    dbo.collection("butterflies").findOne(query).then((result)=> {
        db.close();
        console.log(result);
        res.send(result);
    }).catch((err)=> {
        console.log(err);
    });
  });
});

app.post('/searchResult', upload.single("image"), function(req, res, next){
	let link = "http://en.wikipedia.org/wiki/" + butterflies[Math.round(Math.random() * 48)];
	res.status(200).send(JSON.stringify({link:link}));
})

//listen for requests on port 80
app.listen(PORT, function(err){if(err) console.log(err)});

(async function(){

  //model = await tf.loadModel(handler);
  //callMe();

})();

function callMe(){

  let test = './test.png'

  getPixels(test, function(err, pixels) {
    if(err) {
      console.log("Bad image path");
      return;
    }

    r_t = []
    g_t = []
    b_t = []

    for (let y = 0; y < pixels.shape[1]; y++) {
      r = []
      g = []
      b = []
      for (let x = 0; x < pixels.shape[0]; x++) {
        r.push(pixels.get(x, y, 0)/255);
        g.push(pixels.get(x, y, 1)/255);
        b.push(pixels.get(x, y, 2)/255);
      }
      r_t.push(r)
      g_t.push(g)
      b_t.push(b)
    }

    img = [r_t, g_t, b_t];

    console.log(img);
  });
  //var imgTensor = tf.tensor(test, [1, 400, 400, 3]);
  //var pred = model.predict(imgTensor).dataSync();
  //console.log(pred);
  console.log("done");

}

function getRandomOne() {
	mongoClient.connect(url, (err, db) => {
		if(err) {throw err;}
  
		let dbo = db.db("bf")
		dbo.collection("butterflies").aggregate([{ $sample: { size: 1 } }]).toArray((err, result) => {
			if (err) {
				console.log(err);
				return;
			}
			else if (!result) {
				console.log("No Result");
				return;
			}
			else {
				db.close();
				console.log(result);
				return result;	
			}
		});
	});
}