document.getElementById('login-switch').addEventListener('click', switchToLogin);
document.getElementById('registration-switch').addEventListener('click',switchToRegistration);
document.getElementById('login-link').addEventListener('click', switchToLogin);
document.getElementById('registration-link').addEventListener('click',switchToRegistration);


function switchToLogin() {
    document.getElementById('login-switch').classList.add('active');
    document.getElementById('login-wrapper').style.display = 'block';

    document.getElementById('registration-switch').classList.remove('active');
    document.getElementById('registration-wrapper').style.display = 'none';
}


function switchToRegistration() {
    document.getElementById('login-switch').classList.remove('active');
    document.getElementById('login-wrapper').style.display = 'none';

    document.getElementById('registration-switch').classList.add('active');
    document.getElementById('registration-wrapper').style.display = 'block';
}


login_form = document.getElementById('login_form');
login_form.addEventListener('submit', event => {
    if (!login_form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
    login_form.classList.add('was-validated')
}, false);


registration_form = document.getElementById('registration_form');
registration_form.addEventListener('submit', event => {
    if (!registration_form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
    registration_form.classList.add('was-validated')
}, false);


function checkMatchingPasswords() {
    let password = document.getElementById('password');
    let password_confirmation = document.getElementById('password_confirmation');

    if (password.value != password_confirmation.value) {
        password_confirmation.setCustomValidity("Passwords don't match");
    } else {
        password_confirmation.setCustomValidity('');
    }
    // password_confirmation.reportValidity();
}

function checkUsernameAvailability() {
    let username = document.getElementById('username');
    if (usernameIsValid(username.value)) {
        fetch('api/username/' + username.value)
        .then(response => response.json())
        .then(data => {
            if (data.available) {
                username.setCustomValidity('');
            }
            else {
                username.setCustomValidity("Username not available.");
                document.getElementById('username-feedback').innerHTML = "Username not available";
            }
        });
    }
    else {
        username.setCustomValidity("Username not valid.");
        document.getElementById('username-feedback').innerHTML = "Username not valid";
    }
}

function usernameIsValid(username) {
    const u = /^[a-zA-Z]+[a-zA-Z0-9\-\.]*$/
    return u.test(username);
}