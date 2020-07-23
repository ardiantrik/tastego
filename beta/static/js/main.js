var base64;


function original() {
	$('#progress').show();
	if ($('#image-up').prop('files')[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			base64 = e.target.result;
			//console.log(base64);
			$('#ori-image').attr('src', base64);
		};
		reader.readAsDataURL($('#image-up').prop('files')[0]);
	}
}


function validateImageSize(){
	if ($('#image-up').prop('files')[0]) {
		var img1 = $('#image-up').prop('files')[0].size;
	console.log(img1);
	var img2 = $('#hiding-up').prop('files')[0].size;
	console.log(img2);
	console.log(img2*3);
	if (img1<=(img2*3)) {
		document.getElementById("encode_gambar").value = 'Ukuran Melebihi Cover!';
		document.getElementById("encode_gambar").disabled = true;
	}else{
		document.getElementById("encode_gambar").value = 'Encode Gambar';
		document.getElementById("encode_gambar").disabled = false;
	}
	} 
	
}

M.AutoInit();

$(document).ready(function(){
	
	$('#textarea2').keyup(function( index ) {
		var img1 = $('#image-up').prop('files')[0].size;
		document.getElementById("textarea2").setAttribute("data-length", parseInt(img1/3));
		let string = $(this).val();
		let totString = string.length;
		if (totString*3>img1) {
			document.getElementById("encode_text").value = 'Teks Melebihi Batas!';
			document.getElementById("encode_text").disabled = true;
		}else{
			document.getElementById("encode_text").value = 'Encode Pesan';
			document.getElementById("encode_text").disabled = false;
		}
		
	});

	$('textarea#textarea2').characterCounter();

	$("#decode_object").click(function (){
		//DO NOT DELETE
		//KANGGO MODAL DECODE
		var fd = new FormData();
		var files = $('#image-up')[0].files[0];
		fd.append('file',files);
		
		$.ajax({
            url: '/go_decode',
            type: 'POST',
            data: fd,
            contentType: false,
            processData: false,
            success: function(response){
                if(response != 0){
					//console.log("success broh");
					//console.log(response);
					var str = String(response);
					var cek = str.includes("data:image;base64,");
					console.log(cek);
					
					if (cek) {
						document.getElementById("hidden_object").innerHTML = '<img src="'+response+'" class="responsive-img" />';
					} else {
						document.getElementById("hidden_object").innerHTML =response;	
					}
					
                }else{
                    alert('file not uploaded');
                }
            },
        });

	});


});