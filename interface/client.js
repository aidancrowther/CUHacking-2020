var mousePressed = false;
var lastX, lastY;
var ctx;

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");

    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#myCanvas').mouseup(function (e) {
        mousePressed = false;
    });
	    $('#myCanvas').mouseleave(function (e) {
        mousePressed = false;
    });
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.lineWidth = "18";
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}
	
function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function sendNum(){

    let toSend = convertToArray();

    $.post('/getResult', {'image' : toSend}, function(data){
        let max = 0.0;
        let maxR = 0;
        for(let key in data){
            if(data[key] > max){
                max = data[key];
                maxR = key;
            }
        }
        $('#result').html(maxR);
    });

}

function convertToArray(){

    let img = ctx.getImageData(0, 0, 280, 280).data;
    let greyScale = [];

    for(let i=0; i<img.length; i += 4){
        greyScale[i/4] = (img[i+3])/255;
    }

    let twoDRep = [];

    for(let i=0; i<280; i++){
        let toAdd = [];
        for(let j=0; j<280; j++){
            toAdd[j] = greyScale[(i*280)+j];
        }
        twoDRep[i] = toAdd;
    }

    let final = [];

    for(let i=0; i<28; i++){
        for(let j=0; j<28; j++){
            let result = 0.0;
            for(let x=i*10; x<(i*10)+10; x++){
                for(let y=j*10; y<(j*10)+10; y++){
                    result += twoDRep[x][y];
                }
            }
            final[(i*28)+j] = result/100;
        }
    }
    return final;
}