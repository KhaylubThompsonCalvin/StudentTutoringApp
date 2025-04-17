/*
Author: Khaylub Thompson-Calvin
Date: 04/16/2025
File Name: main.js
Description:
Enhanced JavaScript for the Eyes Unclouded App.
Includes animated flash fade-outs, real-time form feedback,
and a foundation for perception-based interaction logic.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 1s ease, transform 0.5s ease';
            msg.style.opacity = 0;
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 1000);
        }, 4000);
    });

    // Character counter for template or message textarea
    const textarea = document.getElementById('template_body') || document.getElementById('message');
    if (textarea) {
        const counter = document.createElement('small');
        counter.classList.add('char-counter');
        textarea.parentNode.appendChild(counter);

        const updateCounter = () => {
            counter.textContent = `${textarea.value.length} characters`;
        };

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    // Live form validation feedback
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#ff5252';
                    hasError = true;
                } else {
                    field.style.borderColor = '#00ffc3';
                }
            });

            if (hasError) {
                e.preventDefault();
                alert("Please fill out all required fields to continue your path.");
            }
        });
    }
});