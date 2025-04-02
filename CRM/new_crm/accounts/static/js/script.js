document.addEventListener('DOMContentLoaded', function() {
    // Scroll Animations (for landing page)
    const elements = document.querySelectorAll('.animate-on-scroll');

    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8
        );
    }

    function handleScroll() {
        elements.forEach(element => {
            if (isInViewport(element)) {
                element.classList.add('visible');
            } else {
                element.classList.remove('visible');
            }
        });
    }

    window.addEventListener('scroll', handleScroll);
    handleScroll();

    // Smooth Scrolling for Navbar Links (for landing page)
    document.querySelectorAll('.nav-link').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Function to show error popup
    function showErrorPopup(popup, messageElement, message) {
        if (popup && messageElement) {
            messageElement.textContent = message;
            popup.classList.add('show');
            setTimeout(() => {
                popup.classList.remove('show');
            }, 2000);
        }
    }

    // Handle backend error messages on page load
    const backendMessagesDiv = document.getElementById('backend-messages');
    if (backendMessagesDiv) {
        const backendErrorMessages = backendMessagesDiv.querySelectorAll('.backend-error-message');
        if (backendErrorMessages.length > 0) {
            const signupErrorPopup = document.getElementById('signup-error-popup');
            const signupErrorMessage = document.getElementById('signup-error-message');
            const loginErrorPopup = document.getElementById('login-error-popup');
            const loginErrorMessage = document.getElementById('login-error-message');

            // Determine which page we're on and use the appropriate popup
            const popup = signupErrorPopup || loginErrorPopup;
            const messageElement = signupErrorMessage || loginErrorMessage;

            if (popup && messageElement) {
                backendErrorMessages.forEach(message => {
                    showErrorPopup(popup, messageElement, message.textContent);
                });
            }
        }
    }

    // Signup Form Validation
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        const signupErrorPopup = document.getElementById('signup-error-popup');
        const signupErrorMessage = document.getElementById('signup-error-message');

        signupForm.addEventListener('submit', function(e) {
            const fullName = document.getElementById('full-name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            // Basic client-side validation
            if (!fullName.trim()) {
                e.preventDefault(); // Prevent form submission
                showErrorPopup(signupErrorPopup, signupErrorMessage, 'Please enter your full name!');
            } else if (password !== confirmPassword) {
                e.preventDefault(); // Prevent form submission
                showErrorPopup(signupErrorPopup, signupErrorMessage, 'Passwords do not match!');
            } else if (!email.includes('@')) {
                e.preventDefault(); // Prevent form submission
                showErrorPopup(signupErrorPopup, signupErrorMessage, 'Please enter a valid email!');
            }
            // If all validations pass, the form will submit naturally, and the backend will handle the redirect
        });
    }

    // Login Form Validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        const loginErrorPopup = document.getElementById('login-error-popup');
        const loginErrorMessage = document.getElementById('login-error-message');

        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Basic client-side validation
            if (!email.includes('@')) {
                e.preventDefault(); // Prevent form submission
                showErrorPopup(loginErrorPopup, loginErrorMessage, 'Please enter a valid email!');
            } else if (password.length < 6) {
                e.preventDefault(); // Prevent form submission
                showErrorPopup(loginErrorPopup, loginErrorMessage, 'Password must be at least 6 characters!');
            }
            // If all validations pass, the form will submit naturally, and the backend will handle the redirect
        });
    }
});