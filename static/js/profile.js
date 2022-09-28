$(document).ready(
getprops()
);


function getprops() {
  $.ajax({
    url: "/getProps",
    method: "POST",
    success: function (data) {
      var html_to_append = '';
      $.each(data, function (i, item) {
        html_to_append +=
          '<p id=' + i + '>' + item + ' <a href=\"javascript:del_prop(' + i + ');\">Διαγραφή</a></p>';
      });
      $("#items-container").html(html_to_append);
    }
  })
}

function del_prop(id) {
    $.post( "/delprop", {
    del_id: id,
    success: function (response) {
        console.log('Item ' + id + ' deleted');
        alert('Η αγγελία διεγράφη επιτυχώς')
        document.getElementById(id).remove();
    },
    error: function(error){
        console.log(error);
    }
    })
}

function clear_fields() {
    document.getElementById('inputprice').value = "";
    document.getElementById('inputarea').value = "";
}

$(function(){
	$('button').click(function(e){
		var price = $('#inputprice').val();
		var city = $('#inputcity').val();
		var avail = $('#inputavail').val();
		var area = $('#inputarea').val();
		$.ajax({
			url: '/saveProp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
			    getprops();
			    clear_fields();
			    alert('H αγγελία αποθηκεύτηκε επιτυχώς')
				console.log(response);
			},
			error: function(error){
			    alert(error.responseJSON['err'])
				console.log(error.responseJSON['err']);
			}
		});
		e.preventDefault();
	});
});
