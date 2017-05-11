$(function(){
	
	var dropbox = $('#dropbox'),
		message = $('.message', dropbox);

	dropbox.filedrop({
		paramname: 'file',
		maxfiles: 10,
    	maxfilesize: 5,
		url: '/upload',
		uploadFinished:function(i,file,response){
			$.data(file).addClass('done');
		},
		
    	error: function(err, file) {
			switch(err) {
				case 'BrowserNotSupported':
					showMessage('Twoja przegladrka nie wspiera HTML5 uploads!');
					break;
				case 'TooManyFiles':
					alert('Za duzo plikow! Maksymalna ilosc to ' + this.maxfiles + ' !');
					break;
				case 'FileTooLarge':
					alert(file.name + ' Jest zbyt duzy! Maksymalna wielkosc zdjecia to ' + this.maxfilesize + 'MB.');
					break;
				default:
					break;
			}
		},
		
		beforeEach: function(file){
			if(!file.type.match(/^image\//)){
				alert('Only images are allowed!');
				return false;
			}
		},
		
		uploadStarted:function(i, file, len){
			createImage(file);
		},
		
		progressUpdated: function(i, file, progress) {
			$.data(file).find('.progress').width(progress);
		}
    	 
	});
	
	var template = '<div class="preview">'+
						'<span class="imageHolder">'+
							'<img />'+
							'<span class="uploaded"></span>'+
						'</span>'+
						'<div class="progressHolder">'+
							'<div class="progress"></div>'+
						'</div>'+
					'</div>'; 
	
	
	function createImage(file){

		var preview = $(template), 
			image = $('img', preview);
			
		var reader = new FileReader();
		
        image.width = 100;
		image.height = 100;

		reader.onload = function(e){
			image.attr('src',e.target.result);
		};
		
		reader.readAsDataURL(file);
		
		message.hide();
		preview.appendTo(dropbox);
		
		$.data(file,preview);
	}

	function showMessage(msg){
		message.html(msg);
	}

});
