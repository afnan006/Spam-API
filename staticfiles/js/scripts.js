document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const searchForm = document.getElementById('search-form');
    const popup = document.getElementById('popup');

    function showPopup(message) {
        popup.textContent = message;
        popup.classList.add('visible');
        setTimeout(() => {
            popup.classList.remove('visible');
        }, 3000);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const username = document.getElementById('register-username').value;
            const phone = document.getElementById('register-phone').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;

            fetch('http://127.0.0.1:8000/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    phone_number: phone,
                    email: email,
                    password: password,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.username) {
                    showPopup('User registered successfully');
                } else {
                    showPopup('Error: ' + JSON.stringify(data));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const phone = document.getElementById('login-phone').value;
            const password = document.getElementById('login-password').value;

            fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone_number: phone,
                    password: password,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.token) {
                    showPopup('User logged in successfully');
                } else {
                    showPopup('Error: ' + JSON.stringify(data));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }

    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const query = document.getElementById('search-query').value;

            fetch(`http://127.0.0.1:8000/api/search/?query=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${sessionStorage.getItem('token')}`
                }
            })
            .then(response => response.json())
            .then(data => {
                const resultsList = document.getElementById('search-results');
                resultsList.innerHTML = '';

                data.results.forEach(contact => {
                    const li = document.createElement('li');
                    li.textContent = `${contact.name} - ${contact.phone_number} - Spam: ${contact.is_spam}`;
                    resultsList.appendChild(li);
                });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});
