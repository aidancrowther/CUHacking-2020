const tf = require("@tensorflow/tfjs");
const tfn = require("@tensorflow/tfjs-node");
const handler = tfn.io.fileSystem("./model/model.json");
const express = require('express');
var bodyParser = require('body-parser');

var app = express();

//server constants
const ROOT = './interface';
const PORT = 4000;

let model;

var urlEncodedParser = bodyParser.urlencoded({ extended: true });
app.use(express.static('interface'));

//respond to request for index.html
app.get('/', function(req, res){
  res.sendFile( ROOT + '/index.html');
});

app.post('/getResult', urlEncodedParser, function(req, res){
  let image = req.body['image'].map(Number);
  var imgTensor = tf.tensor(image, [1, 28, 28, 1]);
  var pred = model.predict(imgTensor).dataSync();
  res.send(pred);
  for(let i=0; i<28; i++){
    let s = "";
    for(let j=0; j<28; j++){
      if(image[(i*28)+j] > 0) s+='#';
      else s+=' ';
    }
    console.log(s);
  }
  let temp = imgTensor.dataSync();
  for(let i=0; i<28; i++){
    let s = "";
    for(let j=0; j<28; j++){
      if(temp[(i*28)+j] > 0) s+='#';
      else s+=' ';
    }
    console.log(s);
  }
});

//listen for requests on port 80
app.listen(PORT, function(err){if(err) console.log(err)});

(async function(){

  model = await tf.loadModel(handler);
  callMe();

})();

function callMe(){

  /*
  var imgTensor = tf.tensor(test, [1, 28, 28, 1]);
  var pred = model.predict(imgTensor).dataSync();
  console.log(pred);
  console.log("done");
  */

}