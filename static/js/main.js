var base64, base64_2;
var img1D, img2D, lenb, resp;

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
		var img1size = $('#image-up').prop('files')[0].size;
		document.getElementById("sizeOri").innerHTML = "Ukuran File Cover : "+ parseInt(img1size/1000) +" KB";
		img1.src = window.URL.createObjectURL($('#image-up')[0].files[0])
		img1.onload = () => {
			img1D = img1.height*img1.width;
			document.getElementById("pxOri").innerHTML = "Dimensi Cover : " + parseInt(img1.height) + "px X " + parseInt(img1.width) + "px";
			document.getElementById("kapOri").innerHTML = "Kapasistas Cover : " + parseInt((img1D/32)*3);
			if ($('#hiding-up').prop('files')[0]) {
				var img2size = $('#hiding-up').prop('files')[0].size;
				document.getElementById("sizeHidden").innerHTML = "Ukuran File Hidden : "+ parseInt(img2size/1000) +" KB";
				img2.src = window.URL.createObjectURL($('#hiding-up')[0].files[0])
				img2.onload = () => {
					img2D = img2.height*img2.width;
					lenb = base64_2.length;
					document.getElementById("kapHidden").innerHTML = "Kapasistas Hidden : " + parseInt(lenb);
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
function sendPSNR(fd){
	$.ajax({
		url: '/go_hitpsnr',
		type: 'POST',
		data: fd,
		contentType: false,
		processData: false,
		success: function(response){
			if(response != 0){
				console.log("success PSNR");
				console.log(response);
				document.getElementById("idnPSNR").innerHTML = "PSNR : " + response.psnr;
				document.getElementById("idnMSE").innerHTML =  "MSE  : " + response.mse;
				// var str = String(response);
				// var cek = str.includes("data:image/png;base64,");
				// console.log(cek);
				
				// if (cek) {
				// 	document.getElementById("hidden_object").innerHTML = '<img src="'+response+'" class="responsive-img" />';
				// } else {
				// 	document.getElementById("hidden_object").innerHTML =response;	
				// }
				
			}else{
				alert('file not uploaded');
			}
		},
	});
}

function sendDecode(fd, komponenId){
	
	$.ajax({
		url: '/go_decode',
		type: 'POST',
		data: fd,
		contentType: false,
		processData: false,
		success: function(response){
			if(response != 0){
				console.log("success broh");
				// console.log(response);
				var str = String(response);
				var cek = str.includes("data:image/png;base64,");
				console.log(cek);
				
				if (cek) {
					// return '<img src="'+response+'" class="responsive-img" />';
					document.getElementById(komponenId).innerHTML = '<img src="'+response+'" class="responsive-img" />';
				} else {
					console.log(response);
					// return response;
					document.getElementById(komponenId).innerHTML =response;	
				}
				
			}else{
				alert('file not uploaded');
			}
		},
	});
}

$(document).ready(function(){
	
	$('#textarea2').keyup(function( index ) {
		var img1 = new Image();
		if ($('#image-up').prop('files')[0]) {
			img1.src = window.URL.createObjectURL($('#image-up')[0].files[0])
			img1.onload = () => {
				img1D = img1.height*img1.width;
				document.getElementById("textarea2").setAttribute("data-length", parseInt((img1D/32)*3));
				let string = $(this).val();
				let totString = string.length;
				if (totString>((img1D/32)*3)) {
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
		var tipeUp = "file"
		//DO NOT DELETE
		//KANGGO MODAL DECODE
		var fd = new FormData();
		var files = $('#image-up')[0].files[0];
		console.log(files);
		fd.append('file',files);
		fd.append('method',metode);
		fd.append('type',tipeUp);
		
		sendDecode(fd,"hidden_object");

		// $.ajax({
        //     url: '/go_decode',
        //     type: 'POST',
        //     data: fd,
        //     contentType: false,
        //     processData: false,
        //     success: function(response){
        //         if(response != 0){
		// 			//console.log("success broh");
		// 			//console.log(response);
		// 			var str = String(response);
		// 			var cek = str.includes("data:image/png;base64,");
		// 			console.log(cek);
					
		// 			if (cek) {
		// 				document.getElementById("hidden_object").innerHTML = '<img src="'+response+'" class="responsive-img" />';
		// 			} else {
		// 				document.getElementById("hidden_object").innerHTML =response;	
		// 			}
					
        //         }else{
        //             alert('file not uploaded');
        //         }
        //     },
        // });

	});

	$("#decodeHasilLSB").click(function (){
		var loc = document.getElementById("fileLocationLSB").value;
		var met = "LSB";
		var tipeUp = "loc"
		console.log(loc+ " "+ met);
		var fd = new FormData();
		fd.append('location',loc);
		fd.append('method',met);
		fd.append('type',tipeUp);

		sendDecode(fd,"hidden_object");

	});

	$("#decodeHasilDCT").click(function (){
		var loc = document.getElementById("fileLocationDCT").value;
		var met = "DCT";
		var tipeUp = "loc"
		console.log(loc+ " "+ met);
		var fd = new FormData();
		fd.append('location',loc);
		fd.append('method',met);
		fd.append('type',tipeUp);
		
		sendDecode(fd,"hidden_object");

	});

	$("#decodeHasilDWT").click(function (){
		var loc = document.getElementById("fileLocationDWT").value;
		var met = "DWT";
		var tipeUp = "loc"
		console.log(loc+ " "+ met);
		var fd = new FormData();
		fd.append('location',loc);
		fd.append('method',met);
		fd.append('type',tipeUp);
		
		sendDecode(fd,"hidden_object");

	});

	$("#decodeHasilALL").click(function (){
		var loc = document.getElementById("fileLocationALL").value;
		var met = "ALL";
		var tipeUp = "loc"
		console.log(loc+ " "+ met);
		var fd = new FormData();
		fd.append('location',loc);
		fd.append('method',met);
		fd.append('type',tipeUp);
		
		sendDecode(fd,"hidden_object");

	});

	$("#identifyHasil").click(function (){
		if ($('#image-up1').prop('files')[0]) {
			var reader = new FileReader();
			reader.onload = function (e) {
				base64 = e.target.result;
				$('#stegImage1').attr('src', base64);
			};
			reader.readAsDataURL($('#image-up1').prop('files')[0]);
		}

		if ($('#image-up2').prop('files')[0]) {
			var reader = new FileReader();
			reader.onload = function (e) {
				base64_2 = e.target.result;
				$('#stegImage2').attr('src', base64_2);
			};
			reader.readAsDataURL($('#image-up2').prop('files')[0]);
		}

		var metode = $('#select-metode option:selected').val();
		console.log(metode);
		var tipeUp = "file"
		//DO NOT DELETE
		//KANGGO MODAL DECODE
		var fd1 = new FormData();
		var fd2 = new FormData();
		var fd_psnr = new FormData();
		var files1 = $('#image-up1')[0].files[0];
		var files2 = $('#image-up2')[0].files[0];
		// console.log(files);
		fd_psnr.append('file1',files1);
		fd_psnr.append('file2',files2);
		sendPSNR(fd_psnr);

		fd1.append('file',files1);
		fd1.append('method',metode);
		fd1.append('type',tipeUp);

		fd2.append('file',files2);
		fd2.append('method',metode);
		fd2.append('type',tipeUp);
		sendDecode(fd1, "hidObject1");
		sendDecode(fd2, "hidObject2");

	});


});