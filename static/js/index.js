const refreshBtn = document.getElementById("refresh__btn");

function refreshImg() {
    req = $.ajax({
        url : '/refreshimg',
        type : 'POST',
    });
  
    req.done(function(data){
        console.log(data);
    });
}