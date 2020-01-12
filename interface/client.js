function readURL(input) {
    console.log(input.files[0]);
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imageContainer-empty').attr('src', e.target.result);
        }
  
        reader.readAsDataURL(input.files[0]);

        let formData = new FormData();
        formData.append("image", input.files[0]);
        console.log(formData);

        $.ajax({
            url: 'http://localhost:4000/searchResult',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            successs: function() {
                console.log('success');
            },
            error: function() {
              console.log('error');
            }
        })
    }
}

$(document).ready(function() {      
    $("#imageField").change(function() {
        console.log("STARTING");
        let clear = document.getElementById("clear-dis");
        clear.id = "clear-ena";
        readURL(this);
    });
    $("#clear-dis").click(function() {
        clearImage();
    })
});

function clearImage(e) {
    let imageContainer = document.getElementById('imageContainer');

    if(imageContainer) {
        imageContainer.innerHTML = '<img alt="Click here to upload..." id="imageContainer">';
        imageContainer.id = "imageContainer";
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