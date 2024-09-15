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



const userQuery = document.querySelector('#query-field');

userQuery.addEventListener('keydown', function(event) {
    if (event.key === 'Enter'){
        event.preventDefault();
        sendQueryOpenAIView(userQuery);
    };
});


const buttonSubmitQuery = document.querySelector('#button-submit-query');
buttonSubmitQuery.addEventListener('click', function() {
    console.log('aaa')
    sendQueryOpenAIView(userQuery);
});

function sendQueryOpenAIView() {
    console.log('bbbb')
    const userAnswer = document.querySelector('#answer-field');
    /* Prevents backend calls and therefore DB calls when the user hasn't input a question */
    if (userQuery.textContent.length < 10 || userQuery.textContent === ' ') {
        userAnswer.innerHTML = 'You need to input a query.';
        return;
        }
    
    userAnswer.innerHTML = '';
    document.querySelector('#spinner').style.display = 'flex';
    const csrfToken = getCookie('csrftoken');
    fetch('/open-ai-connect/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            userQuery: userQuery.textContent
        })
    })
    .then(function(response) { 
        
        return response.text()})
    .then(function(answer) {
        document.querySelector('#spinner').style.display = 'none';
        document.querySelector('#answer-field').innerHTML = answer;
    })
    .catch(function(error) {
        console.error('Error:', error)
    });
};


function initializeScripts() {
    grabDropdownButtons();

}

window.addEventListener("load", function() {
    initializeScripts();
});
