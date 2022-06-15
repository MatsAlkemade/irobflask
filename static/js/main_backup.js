document.getElementById('qr-reader').style.width = "360px";

const html5QrcodeScanner = new Html5Qrcode("qr-reader");
const config = {
  fps: 10,
  aspectRatio: 1.0,
};

var scanCooldown = false;
const cooldownBanner = document.getElementById("cooldownBanner");

function qrCodeSuccessCallback(decodedText, decodedResult){
  if(scanCooldown == false){
    scanCooldown = true;
    cooldownBanner.style.display = "flex";

    document.getElementById("barcodeResult").innerHTML = decodedResult.result.text;
    document.getElementById("productcode").setAttribute("value", decodedResult.result.text);
  
    var productcode = document.getElementById("productcode").getAttribute("value");
  
    req = $.ajax({
      url : '/',
      type : 'POST',
      data : { productcode : productcode }
    });
  
    req.done(function(data){
      setTimeout(() => {
        const productList = document.getElementById("productlist__table");
      
        const row = productList.insertRow(-1);
        row.setAttribute("id",data.id);
    
        const cell1 = row.insertCell(0);
        cell1.innerHTML = data.productcode;
    
        const cell2 = row.insertCell(1);
        cell2.innerHTML = data.date_created;
    
        const cell3 = row.insertCell(2);
        const node_btn = document.createElement("button");
        node_btn.innerHTML = "Verwijder";
        node_btn.setAttribute("class","productlist__btn");
        node_btn.setAttribute("onclick","deleteProduct("+data.id+")");
        cell3.appendChild(node_btn);
      }, 1000);

      setTimeout(() => {
        scanCooldown = false;
        cooldownBanner.style.display = "none";
      }, 1500);
    });
  }
}

function deleteProduct(id){
  req = $.ajax({
    url : '/delete/' + id,
    type : 'DELETE',
    data : { id : id }
  });

  req.done(function(data){
    const tr = document.getElementById(data.id);
    if (tr.parentNode) {
      tr.parentNode.removeChild(tr);
    }
  });
}

html5QrcodeScanner.start(
  { facingMode: "environment"},
  config,
  qrCodeSuccessCallback
);