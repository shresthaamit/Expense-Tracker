function togglePopup(event) {
    event.preventDefault();
    var popup = document.getElementById("login-popup");
    if (window.getComputedStyle(popup).display === "none") {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
}
function tasklistpopup(event) {
    event.preventDefault();
    var popup = document.getElementById("listcat");
    var conclass = document.querySelector(".containerclass")
    if (window.getComputedStyle(popup).display === "none") {
        popup.style.display = "block";
        conclass.style.height = "130px";
    } else {
        popup.style.display = "none";
        conclass.style.height = "100px";
    }
}
function opensource2(event) {
    event.preventDefault();
    var popup = document.getElementById("incsource2");
    if (window.getComputedStyle(popup).display === "none") {
        popup.style.display = "block";
      
    } else {
        popup.style.display = "none";
    }
}
function opensource3(event) {
    event.preventDefault();
    var popup = document.getElementById("incsource3");
    if (window.getComputedStyle(popup).display === "none") {
        popup.style.display = "block";
      
    } else {
        popup.style.display = "none";
    }
}