function showMenu() {
    document.getElementsByClassName("mobile-links")[0].classList.add("menu-anim");
    document.getElementsByClassName("mobile-links")[0].style.visibility = "visible"; 
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  

async function hideMenu() {
    document.getElementsByClassName("mobile-links")[0].classList.add("menu-back");
    await sleep(700);
    document.getElementsByClassName("mobile-links")[0].style.visibility = "hidden"; 
    document.getElementsByClassName("mobile-links")[0].classList.remove("menu-anim");
    document.getElementsByClassName("mobile-links")[0].classList.remove("menu-back");
}
