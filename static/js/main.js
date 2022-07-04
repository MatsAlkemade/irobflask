const navList = document.getElementById("navList");

function openNav(){
  if (navList.style.display === "block") {
    navList.style.display = "none";
  } else {
    navList.style.display = "block";
  }
}