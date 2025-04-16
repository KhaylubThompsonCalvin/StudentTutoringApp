// main.js - Global client-side interactions for the Food Pantry Notification System
document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 1s ease';
            msg.style.opacity = 0;
            setTimeout(() => msg.remove(), 1000);
        }, 4000);
    });

    // Character counter for textarea fields
    const textarea = document.getElementById('template_body') || document.getElementById('message');
    if (textarea) {
        const counter = document.createElement('small');
        counter.style.display = 'block';
        counter.style.marginTop = '5px';
        counter.style.fontSize = '0.85em';
        counter.style.color = '#888';
        textarea.parentNode.appendChild(counter);
        textarea.addEventListener('input', () => {
            counter.textContent = `${textarea.value.length} characters`;
        });
    }

    // Simple form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'crimson';
                    hasError = true;
                } else {
                    field.style.borderColor = '';
                }
            });
            if (hasError) {
                e.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    }
});

