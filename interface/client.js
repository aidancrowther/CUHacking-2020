$(document).ready(function() {
    let upload;

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
    
            let iC = document.getElementById("imageContainer-empty");
            iC.id = "imageContainer";
    
            reader.onload = function(e) {
                upload.croppie('bind', {
                    url: e.target.result
                });
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    upload = $('#imageContainer-empty').croppie({
        viewport: {
            width: 400,
            height: 400,
        },
        boundary: {
            width: 500,
            height: 500,
        },
        showZoomer: false,
        enableOrientation: true

    });

    $('#imageField').on('change', function () { 
        readURL(this);
        let clear = document.getElementById("clear-dis");
        clear.id = "clear-ena";
    });
    $('#upload').on("click", function(ev) {
        upload.croppie('result', {
            type: 'blob',
            size: {width: 400, height: 400}
        }).then(function (resp) {
            $('#item-img-output').attr('src', resp);
            $('#imagebase64').val(resp);
            console.log(resp);
            let clear = document.getElementById("clear-ena");
            clear.id = "clear-dis";
    
            let formData = new FormData();
            formData.append("image", resp);
            
            console.log("Before AJAX");
            $.ajax({
                url: 'http://' + location.host + '/searchResult',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(result,status,xhr) {
                    let success = document.getElementById("success");
                    success.style.color = "green";
                    success.style.fontSize = "150%";
                    success.innerHTML = "Image Added Successfully";
                    success.class = "";

                    let response = JSON.parse(result);
                    window.open(response.link, "_blank");
                },
                error: function(xhr,status,err) {
                    let error = document.getElementById("success");
                    error.style.color = "red";
                    error.style.fontSize = "150%";
                    error.innerHTML = "Uh oh, something went wrong";
                    error.class = "";
                }
            });
        });
    });

    $("#clear-dis").click(function() {
        clearImage();
    })
});

function clearImage() {
    let imageOutput = document.getElementById('item-img-output');

    if(imageOutput) {
        let clear = document.getElementById("clear-ena");
        clear.id = "clear-dis";
        let context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
    }
}