
// Handles opening and closing dropdown menus.
function dropdownMenus(event) {
    const allDropdownMenus = document.querySelectorAll('.dropdown');
    allDropdownMenus.forEach(function(dropdownMenu) {
        dropdownMenu.style.display = 'none';
    })
    const dropdownButton = event.target;
    const dropdownContainer = dropdownButton.closest('.dropdown-container');
    const dropdown = dropdownContainer.querySelector('.dropdown');
    if (getComputedStyle(dropdown).display === 'none'){
            dropdown.style.display = 'flex' ;
    }
    else {
            dropdown.style.display = 'none';
    }
}

function grabDropdownButtons() {
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    dropdownButtons.forEach(function(dropdownButton) {
        dropdownButton.addEventListener('click', dropdownMenus);
    });
};

// Grabs cookie from browser so that it can later be parsed to extract csrf token for POST request.
function getCookie(name) {
    const cookieString = `${document.cookie}`;
    const cookieStringSplit = cookieString.split(`${name}=`);
    return cookieStringSplit.pop().split(';').shift()
    }


// Detects if Enter was pressed while in the input field (to send query).
function detectInputEnter() {
    const userQuery = document.querySelector('#query-field');

     // Call function that sends query to backend, and calls function to disable enter input temporarily
    function handleSubmitEnter(event) {
        if (event.key === 'Enter'){
            event.preventDefault();
            sendQueryOpenAIView(userQuery);
            disableEnterTemporary();
        };
    };

    // Disables 'Enter' input temporarily to prevent quick double presses of 'Enter' key
    function disableEnterTemporary() {
        userQuery.blur();
        userQuery.disabled = true;
        setTimeout(function() {
            userQuery.disabled = false;
        }, 2000);
    };

    userQuery.addEventListener('keydown', handleSubmitEnter);
}

// Detects if submit button (to send query) was clicked.
function detectInputClick() {
    const userQuery = document.querySelector('#query-field');
    const buttonSubmitQuery = document.querySelector('#button-submit-query');

    // Call function that sends query to backend, and calls function to disable submit button temporarily
    function handleSubmitClick() {
        sendQueryOpenAIView(userQuery);
        disableSubmitButtonTemporary(buttonSubmitQuery, 3000);
    }
    // Disables submit button temporarily to prevent quick double clicks.
    function disableSubmitButtonTemporary() {
        userQuery.blur();
        buttonSubmitQuery.disabled = true;
        setTimeout(function() {
            buttonSubmitQuery.disabled = false;
        }, 2000);
    };

    buttonSubmitQuery.addEventListener('click', handleSubmitClick);
};

// Sends query to backend view that calls Open AI API.
function sendQueryOpenAIView(userQuery) {
    const userAnswer = document.querySelector('#answer-field');

    // Prevents backend calls and therefore DB calls when the user hasn't input a question.
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

// Handles opening and closing the nav menu button, as well as the nav menu itself.
function openCloseNavMenuButtonMobile() {
    const mobileNavMenuButtonOpen = document.querySelector('#mobile-open-nav');
    const mobileNavMenuButtonClose = document.querySelector('#mobile-close-nav');
    const mobileNavMenu = document.querySelector('#nav-inner ul');

    mobileNavMenuButtonOpen.addEventListener('click', function() {
        mobileNavMenu.style.display = 'flex';
        mobileNavMenuButtonOpen.style.display = 'none';
        mobileNavMenuButtonClose.style.display = 'flex';
        
    })

    mobileNavMenuButtonClose.addEventListener('click', function() {
        mobileNavMenu.style.display = 'none';
        mobileNavMenuButtonClose.style.display = 'none';
        mobileNavMenuButtonOpen.style.display = 'flex';
    })


}

function startScripts() {
    if (document.querySelector('.dropdown')) {
        grabDropdownButtons();
    }
    if (document.querySelector('#query-field')) {
        detectInputClick(); 
        detectInputEnter();
    };
    openCloseNavMenuButtonMobile();

}

window.addEventListener('load', function() {
    startScripts();
});
