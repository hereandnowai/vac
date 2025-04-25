window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-scrolled');
        } else {
            navbarCollapsible.classList.add('navbar-scrolled');
        }
    };

    // Shrink the navbar
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74, // Adjust based on navbar height
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Initialize AOS (Animate on Scroll)
    AOS.init({
        duration: 800, // Animation duration
        once: true      // Animation happens only once
    });

    // Counter Animation Function
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // Lower = faster animation

    const animateCounter = (counter) => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;

        const inc = target / speed;

        if (count < target) {
            counter.innerText = Math.ceil(count + inc);
            setTimeout(() => animateCounter(counter), 10); // Adjusted timing
        } else {
            counter.innerText = target; // Ensure it ends exactly at target
        }
    };

    // Intersection Observer for Counters
    const counterSection = document.querySelector('.stats-counters');
    if (counterSection) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    counters.forEach(counter => {
                         // Check if animation has already run
                        if (!counter.classList.contains('animated')) {
                           animateCounter(counter);
                           counter.classList.add('animated'); // Mark as animated
                        }
                    });
                    // Optionally disconnect observer after animation
                    // observer.disconnect();
                }
            });
        }, { threshold: 0.5 }); // Trigger when 50% visible

        observer.observe(counterSection);
    }

    // Smooth scroll for Back to Top button (and potentially other # links if needed)
    const backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Contact Form Submission Placeholder
    const contactForm = document.getElementById('contactForm');
    const formFeedback = document.getElementById('form-feedback');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the default form submission

            // Basic validation check (can be expanded)
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const college = document.getElementById('college').value;
            const message = document.getElementById('message').value;

            if (name && email && college && message) {
                 // Simulate form submission (replace with actual AJAX call later)
                 formFeedback.innerHTML = '<div class="alert alert-success form-success" role="alert">Thank you! Your message has been sent successfully. We will get back to you soon.</div>';
                 contactForm.reset(); // Clear the form

                 // Remove feedback message after a few seconds
                 setTimeout(() => {
                     formFeedback.innerHTML = '';
                 }, 5000);

            } else {
                 formFeedback.innerHTML = '<div class="alert alert-danger form-error" role="alert">Please fill out all required fields.</div>';
                 // Remove feedback message after a few seconds
                  setTimeout(() => {
                     formFeedback.innerHTML = '';
                 }, 5000);
            }
        });
    }

}); // End DOMContentLoaded