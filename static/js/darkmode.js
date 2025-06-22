// static/js/darkmode.js
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');

    // On page load, apply saved theme from localStorage
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }

    // Toggle theme on button click
    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
});
