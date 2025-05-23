document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
            if (form.checkValidity()) {
                const button = form.querySelector('button[type="submit"]');
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Kirish';
                button.disabled = true;
                setTimeout(() => {
                    button.innerHTML = 'Kirish';
                    button.disabled = false;
                }, 2000); // Simulate loading
            }
        }, false);
    });

    // ... (keep existing dynamic search and delete confirmation code)
});