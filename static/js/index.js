const refreshBtn = document.getElementById("refresh__btn");

function refreshImg() {
    $.ajax({
        type : "POST",
        url : 'refreshimg',
        success : callbackFunc
    });
}

function callbackFunc(response){
    console.log(response);
    window.location.reload();
}