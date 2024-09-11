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
    dropdownButtons.forEach(function(dropdownButton) {
        dropdownButton.addEventListener('click', dropdownMenus);
    });
};

function getCookie(name) {
    const cookieString = `${document.cookie}`;
    const cookieStringSplit = cookieString.split(`${name}=`);
    return cookieStringSplit.pop().split(';').shift()
    }

function sendQueryOpenAIView() {
    const csrfToken = getCookie('csrftoken');
    const buttonSubmitQuery = document.querySelector('#button-submit-query');
    buttonSubmitQuery.addEventListener('click', function() {
    const userQuery = document.querySelector('#query-field').textContent;
    console.log(userQuery)
    

    fetch('/open-ai-connect/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            userQuery: userQuery
        })
    })
   .then(function(response) { 
    response.json()})
   .then(function (json) {

   });
});
};


function initializeScripts() {
    grabDropdownButtons();
    sendQueryOpenAIView();
}

window.addEventListener("load", function() {
    initializeScripts();
});