document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.lead-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const gender = document.querySelector('select[name="gender"]').value;
            if (!['Male', 'Female', 'Other'].includes(gender)) {
                e.preventDefault();
                alert("Please select a valid gender.");
            }
        });
    }
});