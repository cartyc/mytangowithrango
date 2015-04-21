$(document).ready( function(){

	$('#likes').click(function(){
		var categoryid;
		categoryid = $(this).attr("data-catid");
		$.get('/rango/like_category/', { category_id: categoryid}, function(data){
			$('#like_count').html(data);
			$('#likes').hide();
		});
	});

})