function matchTemplates() {
    $.ajax({
        type : "POST",
        url : "python",
        data : {
            function : "matchtemplates",
        },
        success : callbackFunc
    });
}

function callbackFunc(response){
    console.log(response);
    window.location.reload();
}