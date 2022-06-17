document.getElementById('qr-reader').style.width = "360px";

const html5QrcodeScanner = new Html5Qrcode("qr-reader");
const config = {
  fps: 10,
  aspectRatio: 1.0,
};

var scanCooldown = false;
const cooldownBanner = document.getElementById("cooldownBanner");

const bcModal = document.getElementById("bcModal");
const closeBcModalBtn = document.getElementById("closeBcModalBtn");
const bcSaveBtn = document.getElementById("bcSaveBtn");
const modalScanBc = document.getElementById("modalScanBc");
const modalMakeBg = document.getElementById("modalMakeBg");
const modalMakeNewInv = document.getElementById("modalMakeNewInv");

function qrCodeSuccessCallback(decodedText, decodedResult){
  if(scanCooldown == false){
    scanCooldown = true;
    cooldownBanner.style.display = "flex";
    openBarcodeModal();
    document.getElementById("barcodeResult").innerHTML = decodedResult.result.text;
    document.getElementById("productcode").value = decodedResult.result.text;
  }
}

function deleteProduct(id){
  req = $.ajax({
    url : '/delete/' + id,
    type : 'DELETE',
    data : { id : id }
  });

  req.done(function(data){
    const tb = document.getElementById("productlist__table__body");
    const tr = document.getElementById(data.id);
    tb.removeChild(tr);
  });
}

function openBarcodeModal(){
    bcModal.style.display = "block";
}

function closeBarcodeModal(){
    document.getElementById("productcode").value = "";
    document.getElementById("product_name").value = "";
    bcModal.style.display = "none";
    
    modalScanBc.style.display = "block";
    modalMakeNewInv.style.display = "none";
    modalMakeBg.style.display = "none";
    
    setTimeout(() => {
      scanCooldown = false;
      cooldownBanner.style.display = "none";
    }, 1500);
}

bcSaveBtn.onclick = function() {
  if(document.getElementById("productcode").value == "" || document.getElementById("product_name").value == ""){
    document.getElementById("bcRequired").style.color = "rgba(255,0,0,1)";
  } else {
    saveBarcode();
  }
  setTimeout(() => {
    document.getElementById("bcRequired").style.color = "rgba(255,0,0,0)";
  }, 1000);
}

function saveBarcode() {
    var productcode = document.getElementById("productcode").value;
    var product_name = document.getElementById("product_name").value;
    
    req = $.ajax({
      url : '/',
      type : 'POST',
      data : {
        productcode : productcode,
        product_name : product_name,
        }
    });
  
    req.done(function(data){
      setTimeout(() => {
        const productList = document.getElementById("productlist__table__body");
      
        const row = productList.insertRow(-1);
        row.setAttribute("id",data.id);
        
        const cell1 = row.insertCell(0);
        cell1.innerHTML = data.product_name;
    
        const cell2 = row.insertCell(1);
        cell2.innerHTML = data.productcode;
    
        const cell3 = row.insertCell(2);
        cell3.innerHTML = data.date_created;
    
        const cell4 = row.insertCell(3);
        const node_btn = document.createElement("button");
        node_btn.innerHTML = "Verwijder";
        node_btn.setAttribute("class","productlist__btn");
        node_btn.setAttribute("onclick","deleteProduct("+data.id+")");
        cell4.appendChild(node_btn);
      }, 1000);
      
      openModalBg();
    });
}

function openModalBg() {
  modalScanBc.style.display = "none";
  modalMakeBg.style.display = "block";
}

function openModalNewInv() {
  // Code om python script te runnen background maken
  
  modalMakeBg.style.display = "none";
  modalMakeNewInv.style.display = "block";
}

function makeTemplate(){
  // Code om python script te runnen template maken
  
  closeBarcodeModal();
}

closeBcModalBtn.onclick = function() {
  closeBarcodeModal();
}

window.onclick = function(event) {
  if (event.target == bcModal) {
    closeBarcodeModal();
  }
}

window.onload = function(event) {
  callPyFunc("hoi");
}

function callPyFunc(input) {
  $.ajax({
      type: "POST",
      url: "/python",
      data: { func: input },
  });
}

html5QrcodeScanner.start(
  { facingMode: "environment"},
  config,
  qrCodeSuccessCallback
);
