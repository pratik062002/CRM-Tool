document.addEventListener('DOMContentLoaded', function() {
    // Scroll Animations
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

    // Smooth Scrolling for Navbar Links
    document.querySelectorAll('.nav-link').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            // Only apply smooth scrolling for links starting with '#'
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
            // For non '#' links (like 'login'), let the default behavior (redirect) happen
        });
    });
});