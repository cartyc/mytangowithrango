// $(document).ready( function(){

// 	$("#about-btn").click(function(event){
// 		alert("You clicked the button using JQUERY!");
// 	});
// });

$(document).ready( function() {

    $("#about-btn").addClass('btn btn-primary');

	    $("#about-btn").click( function(event){
		msgstr = $("#msg").html()
		msgstr = msgstr + "0"
		$("#msg").html(msgstr)
	});
});

