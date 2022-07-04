function refreshImg() {
    $.ajax({
        type : 'POST',
        url : 'python',
        data : {
            function : 'refreshimg'
        },
        success : callbackFunc
    });
}

function callbackFunc(response){
    console.log(response);
    window.location.reload();
}