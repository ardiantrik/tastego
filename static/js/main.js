var base64, base64_2;
var img1D, img2D, lenb;

function original() {
	$('#progress').show();
	if ($('#image-up').prop('files')[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			base64 = e.target.result;
			// console.log(base64);
			$('#ori-image').attr('src', base64);
		};
		reader.readAsDataURL($('#image-up').prop('files')[0]);
	}
}

function hiddenimg() {
	$('#progress').show();
	if ($('#hiding-up').prop('files')[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			base64_2 = e.target.result;
			console.log(base64_2);
			$('#hid-image').attr('src', base64_2);
		};
		reader.readAsDataURL($('#hiding-up').prop('files')[0]);
	}
}



function validateImageSize(){
	
	let img2 = new Image();
	var img1 = new Image();
	
	if ($('#image-up').prop('files')[0]) {
		img1.src = window.URL.createObjectURL($('#image-up')[0].files[0])
		img1.onload = () => {
			img1D = img1.height*img1.width;
			if ($('#hiding-up').prop('files')[0]) {
				img2.src = window.URL.createObjectURL($('#hiding-up')[0].files[0])
				img2.onload = () => {
					img2D = img2.height*img2.width;
					lenb = base64_2.length;
					console.log((img1D/32)*3);
					console.log(lenb);
					// why 32? 1 gambar bagi 8x8 , trus bagi meneh 4 bagian DWT
					if (parseInt((img1D/32)*3)<=lenb) {
						document.getElementById("encode_gambar").value = 'Ukuran Melebihi Cover!';
						document.getElementById("encode_gambar").disabled = true;
					}else{
						document.getElementById("encode_gambar").value = 'Encode Gambar';
						document.getElementById("encode_gambar").disabled = false;
					}
				}
			}
		}
	}
	// if ($('#hiding-up').prop('files')[0]) {
	// 	img2.src = window.URL.createObjectURL($('#hiding-up')[0].files[0])
	// 	img2.onload = () => {
	// 		img2D = img2.height*img2.width;
	// 		console.log(img2D);
	// 		//alert(img.width + " " + img.height);
	// 	}
	// }
	
	// if (img1D) {
	// 	document.getElementById("encode_gambar").value = 'Ukuran Melebihi Cover!';
	// 	document.getElementById("encode_gambar").disabled = true;
	// }else{
	// 	document.getElementById("encode_gambar").value = 'Encode Gambar';
	// 	document.getElementById("encode_gambar").disabled = false;
	// }
	 
	
}

M.AutoInit();
//var instance = M.FormSelect.getInstance(elem);

$(document).ready(function(){
	
	$('#textarea2').keyup(function( index ) {
		var img1 = new Image();
		if ($('#image-up').prop('files')[0]) {
			img1.src = window.URL.createObjectURL($('#image-up')[0].files[0])
			img1.onload = () => {
				img1D = img1.height*img1.width;
				document.getElementById("textarea2").setAttribute("data-length", parseInt(img1D/24));
				let string = $(this).val();
				let totString = string.length;
				if (totString>(img1D/32)) {
					document.getElementById("encode_text").value = 'Teks Melebihi Batas!';
					document.getElementById("encode_text").disabled = true;
				}else{
					document.getElementById("encode_text").value = 'Encode Pesan';
					document.getElementById("encode_text").disabled = false;
				}

			}
		}
		// var img1 = $('#image-up').prop('files')[0].size;
		// document.getElementById("textarea2").setAttribute("data-length", parseInt(img1/3));

	});

	$('textarea#textarea2').characterCounter();

	$("#decode_object").click(function (){
		var metode = $('#select-metode option:selected').val();
		console.log(metode);
		//DO NOT DELETE
		//KANGGO MODAL DECODE
		var fd = new FormData();
		var files = $('#image-up')[0].files[0];
		console.log(files);
		fd.append('file',files);
		fd.append('method',metode);
		
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
					var cek = str.includes("data:image/png;base64,");
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