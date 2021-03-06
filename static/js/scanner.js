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
const bgBtn = document.getElementById("bgBtn");
const newInvBtn = document.getElementById("newInvBtn");
const modalScanBc = document.getElementById("modalScanBc");
const modalMakeBg = document.getElementById("modalMakeBg");
const modalMakeNewInv = document.getElementById("modalMakeNewInv");

function qrCodeSuccessCallback(decodedText, decodedResult){
    if(scanCooldown == false){
        scanCooldown = true;
        cooldownBanner.style.display = "flex";
        openBarcodeModal();
        document.getElementById("barcode").value = decodedResult.result.text;
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
    document.getElementById("barcode").value = "";
    document.getElementById("product_name").value = "";
    document.getElementById("templateError").style.display = "none";

    bcModal.style.display = "none";
    
    bcSaveBtn.disabled = false;
    bgBtn.disabled = false;
    newInvBtn.disabled = false;
  
    modalScanBc.style.display = "block";
    modalMakeNewInv.style.display = "none";
    modalMakeBg.style.display = "none";
      
    setTimeout(() => {
        scanCooldown = false;
        cooldownBanner.style.display = "none";
    }, 1500);
}
  
bcSaveBtn.onclick = function() {
    bcSaveBtn.disabled = true;
    if(document.getElementById("barcode").value == "" || document.getElementById("product_name").value == ""){
        document.getElementById("bcRequired").style.color = "rgba(255,0,0,1)";
        bcSaveBtn.disabled = false;
    } else {
        saveBarcode();
    }
    setTimeout(() => {
        document.getElementById("bcRequired").style.color = "rgba(255,0,0,0)";
    }, 2000);
}
  
function saveBarcode() {
    var barcode = document.getElementById("barcode").value;
    var product_name = document.getElementById("product_name").value;
      
    req = $.ajax({
        url : '/scanner',
        type : 'POST',
        data : {
            barcode : barcode,
            product_name : product_name,
        }
    });
    
    req.done(function(data){
        if(data == "Error"){
            closeBarcodeModal();
            console.log("Er is iets fout gegaan bij het template nummer genereren");
        } else{
            setTimeout(() => {
                const productList = document.getElementById("productlist__table__body");
            
                const row = productList.insertRow(-1);
                row.setAttribute("id",data.id);
            
                const cell1 = row.insertCell(0);
                cell1.innerHTML = data.product_name;
        
                const cell2 = row.insertCell(1);
                cell2.innerHTML = data.barcode;
        
                const cell3 = row.insertCell(2);
                cell3.innerHTML = data.datetime_created;
        
                const cell4 = row.insertCell(3);
                const node_btn = document.createElement("button");
                node_btn.innerHTML = "Verwijder";
                node_btn.setAttribute("class","productlist__btn");
                node_btn.setAttribute("onclick","deleteProduct("+data.id+")");
                cell4.appendChild(node_btn);
            }, 1000);
            bcSaveBtn.disabled = false;
            openModalBg();
        }
    });
}
  
function openModalBg() {
    modalScanBc.style.display = "none";
    modalMakeBg.style.display = "block";
}
  
function openModalNewInv() {
    bgBtn.disabled = true;
    // Code om python script te runnen background maken
    req = $.ajax({
        url : '/python',
        type : 'POST',
        data : {
            function : 'background',
        }
    });

    req.done(function(data){
        console.log(data);
        modalMakeBg.style.display = "none";
        modalMakeNewInv.style.display = "block";
        document.getElementById("templateError").style.display = "none";
        newInvBtn.disabled = false;
        bgBtn.disabled = false;
    });
}
  
function makeTemplate(){
    newInvBtn.disabled = true;
    // Code om python script te runnen template maken
    req = $.ajax({
        url : '/python',
        type : 'POST',
        data : {
            function : 'template',
        }
    });

    req.done(function(data){
        console.log(data);
        if (data == "S"){
            closeBarcodeModal();
        } else {
            document.getElementById("templateError").style.display = "block";
            modalMakeBg.style.display = "block";
            modalMakeNewInv.style.display = "none";
        }
    });
}
  
closeBcModalBtn.onclick = function() {
    closeBarcodeModal();
}
  
window.onclick = function(event) {
    if (event.target == bcModal) {
        closeBarcodeModal();
    }
}
  
html5QrcodeScanner.start(
    { facingMode: "environment"},
    config,
    qrCodeSuccessCallback
);