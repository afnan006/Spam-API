document.addEventListener('DOMContentLoaded', () => {
    const addContactForm = document.getElementById('add-contact-form');
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const searchForm = document.getElementById('search-form');
    const reportSpamForm = document.getElementById('report-spam-form');
    const popup = document.getElementById('popup');

    function showPopup(message) {
        popup.textContent = message;
        popup.classList.add('visible');
        setTimeout(() => {
            popup.classList.remove('visible');
        }, 3000);
    }

    function getCSRFToken() {
        let cookieValue = null;
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (addContactForm) {
        addContactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(addContactForm);
            const data = {
                name: formData.get('name'),
                phone_number: formData.get('phone_number'),
                is_spam: formData.get('is_spam') === 'on' // Convert checkbox value to boolean
            };

            fetch('/api/add-contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${sessionStorage.getItem('token')}`,
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    showPopup('Contact added successfully');
                    addContactForm.reset(); // Reset form after successful submission
                } else {
                    showPopup('Error adding contact: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopup('An error occurred: ' + error.message);
            });
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const username = document.getElementById('register-username').value;
            const phone = document.getElementById('register-phone').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;

            fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
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
                    showPopup('User registered successfully!');
                } else {
                    showPopup('Registration failed: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopup('An error occurred.');
            });
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const phone = document.getElementById('login-phone').value;
            const password = document.getElementById('login-password').value;

            fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    phone_number: phone,
                    password: password,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.token) {
                    showPopup('User logged in successfully!');
                    sessionStorage.setItem('token', data.token);
                } else {
                    showPopup('Login failed: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopup('An error occurred.');
            });
        });
    }

    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const query = document.getElementById('search-query').value;

            fetch(`/api/search/?query=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${sessionStorage.getItem('token')}`
                }
            })
            .then(response => response.json())
            .then(data => {
                const resultsList = document.getElementById('search-results');
                resultsList.innerHTML = '';

                if (data.results && Array.isArray(data.results)) {
                    data.results.forEach(contact => {
                        const li = document.createElement('li');
                        const spamStatus = contact.is_spam ? 'Spam' : 'Not Spam';
                        li.textContent = `${contact.name} - ${contact.phone_number} - ${spamStatus}`;
                        resultsList.appendChild(li);
                    });
                } else {
                    showPopup('No results found.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopup('An error occurred.');
            });
        });
    }

    if (reportSpamForm) {
        reportSpamForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const phone = document.getElementById('report-phone').value;

            fetch('/api/mark-spam/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${sessionStorage.getItem('token')}`,
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    phone_number: phone
                }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    showPopup('Spam reported successfully!');
                } else {
                    showPopup('Report failed: ' + (data.errors || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showPopup('An error occurred: ' + error.message);
            });
        });
    }
});
