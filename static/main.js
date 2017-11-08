$(document).ready(function() {
  console.log("ready!");

  $('#try-again').hide();

  // on form submission ...
  $('form').on('submit', function() {

    console.log("the form has beeen submitted");

    // grab values
    valueOne = $('textarea[name="location"]').val();
    //valueTwo = $('input[name="language"]').val();
    //console.log(valueOne, valueTwo)
    console.log(valueOne);

    $.ajax({
      type: "POST",
      url: "/",
      data : { 'first': valueOne},
      success: function(results) {
        
        console.log(results['results']);
        //$('#results').html('<a href="'+results.items[randNum].html_url+'">'+results.items[randNum].login+
          //    '</a><br><img src="'+results.items[randNum].avatar_url+'" class="avatar">')
        my_result_txt_id = document.getElementById("my_result_txt");
        var str_results = JSON.parse(JSON.stringify(results['results'], undefined, 2));
        var str_best = JSON.parse(JSON.stringify(results['best_match'], undefined, 2));
        my_result_txt_id.value  = ""
	my_result_txt_id.value += "best match: "
        my_result_txt_id.value += str_best;
        my_result_txt_id.value += "\n**************************\n"
	my_result_txt_id.value += "suggestions: "
        my_result_txt_id.value +=  str_results;
                     
      },
      error: function(error) {
        console.log(error);
        my_result_txt_id = document.getElementById("my_result_txt");
        my_result_txt_id.value  = ""
        my_result_txt_id.value += "No Predictions for this word"; 
      }
    });

  });

  $('#try-again').on('click', function(){
    $('input').val('').show();
    $('#try-again').hide();
    $('#results').html('');
  });

});
