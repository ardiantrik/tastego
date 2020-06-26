var base64;
var origin = {
	r: [[]],
	g: [[]],
	b: [[]],
	width: 0,
	height: 0
}
var edited = {
	r: [[]],
	g: [[]],
	b: [[]],
	width: 0,
	height: 0
}
var snd;

function splitstring(str, l) {
	var strs = [];
	var strlen = str.length;
	var tmp = "";
	for (var i = 0; i < strlen; i++) {
		tmp += str[i];
		
		if (tmp.length == l) {
			strs.push(tmp);
			tmp = "";
		}
	}
	strs.push(tmp);
	var result = {jml: strs.length, splitted: strs};
	//console.log(result);
	return result;
}

function original() {
	$('#progress').show();
	if ($('#image-up').prop('files')[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			base64 = e.target.result;
			//console.log(base64);
			$('#ori-image').attr('src', base64);
			snd = splitstring(base64, 1000);
			var rv = {length: snd.jml};
			for (var i = 0; i < snd.jml; i++) {
				var label = "str" + i;
				rv[label] = snd.splitted[i];
			}
			
			$.ajax({
				type: 'POST',
				url: '/image2matrix',
				data: rv,
				success: function(data) {
					data = JSON.parse(data);
					$('#edit-image').attr('src', data.base64);
					$('#progress').hide();
					origin.r = data.r;
					origin.g = data.g;
					origin.b = data.b;
					origin.width = data.width;
					origin.height = data.height;
					edited = origin;
				},
				async: false
			});
		};
		reader.readAsDataURL($('#image-up').prop('files')[0]);
	}
}

function validateSize(){
	var img1 = $('#image-up').prop('files')[0].size;
	var img2 = $('#hidimg-up').prop('files')[0].size;
	if (img1<img2) {
		document.getElementById("encode_gambar").value = 'Ukuran Melebihi Cover!';
		document.getElementById("encode_gambar").disabled = true;
	}else{
		document.getElementById("encode_gambar").value = 'Encode Gambar';
		document.getElementById("encode_gambar").disabled = false;
	}
}

function encode_pesan() {
	if ($('#image-up').prop('files')[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			base64 = e.target.result;
			console.log(base64);
			$('#ori-image').attr('src', base64);
			snd = splitstring(base64, 1000);
			var rv = {length: snd.jml};
			for (var i = 0; i < snd.jml; i++) {
				var label = "str" + i;
				rv[label] = snd.splitted[i];
			}
			
			$.ajax({
				type: 'POST',
				url: 'function/image2matrix.php',
				data: rv,
				success: function(data) {
					data = JSON.parse(data);
					$('#edit-image').attr('src', data.base64);
					$('#progress').hide();
					origin.r = data.r;
					origin.g = data.g;
					origin.b = data.b;
					origin.width = data.width;
					origin.height = data.height;
					edited = origin;
				},
				async: false
			});
		};
		reader.readAsDataURL($('#image-up').prop('files')[0]);
	}
	
}

function grayscale() {
	$('#progress').show();
	$.ajax({
		type: 'POST',
		url: 'function/grayscale.php',
		data: {
			r: JSON.stringify(edited.r),
			g: JSON.stringify(edited.g),
			b: JSON.stringify(edited.b),
			width: edited.width,
			height: edited.height
		},
		success: function(data) {
			data = JSON.parse(data);
			$('#edit-image').attr('src', data.base64);
			$('#progress').hide();
			edited.r = data.r;
			edited.g = data.g;
			edited.b = data.b;
			edited.width = parseInt(data.width);
			edited.height = parseInt(data.height);
		},
		async: false
	});
}

M.AutoInit();

$(document).ready(function(){
	$('#textarea2').keyup(function( index ) {
		let string = $(this).val();
		let totString = string.length;
		if (totString>255) {
			document.getElementById("encode_text").value = 'Teks Melebihi Batas!';
			document.getElementById("encode_text").disabled = true;
		}else{
			document.getElementById("encode_text").value = 'Encode Pesan';
			document.getElementById("encode_text").disabled = false;
		}
		
	});

	$('textarea#textarea2').characterCounter();

	$("#decode_object").click(function (){
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