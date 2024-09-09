function dropdownMenus(event) {
    const dropdownButton = event.target;
    const dropdownContainer = dropdownButton.closest(".dropdown-container");
    if (dropdownContainer){  
        const dropdown = dropdownContainer.querySelector(".dropdown");
        if (getComputedStyle(dropdown).display === "none"){
            dropdown.style.display = "flex" ;
        }
        else {
            dropdown.style.display = "none";
        }
    }

   
}

function grabDropdownButtons() {
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    dropdownButtons.forEach(dropdownButton => {
        dropdownButton.addEventListener('click', dropdownMenus);
    });
};




function initializeScripts() {
    grabDropdownButtons();
}

window.addEventListener("load", () => {
    initializeScripts();
});