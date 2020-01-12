function readURL(input) {
    console.log(input.files[0]);
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imageContainer').attr('src', e.target.result);
        }
  
        reader.readAsDataURL(input.files[0]);
        $.ajax({
            
        })
    }
}

$(document).ready(function() {      
    $("#imageField").change(function() {
        console.log("STARTING");
        readURL(this);
    });
    
    let toSend = null;
    let data = null;

    $.post('/getResult', {'image' : toSend}, function(data){
        console.log('yes');
    });
});

function clearImage(e) {
    if(e) {
        e.preventDefault();
    }

    let imageContainer = document.getElementById('imageContainer');

    console.log(imageContainer);

    if(imageContainer) {
        imageContainer.innerHTML = "";
    }
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