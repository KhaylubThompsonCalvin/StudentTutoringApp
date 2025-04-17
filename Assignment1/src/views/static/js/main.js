/*
 Author: Khaylub Thompson-Calvin
 Date: 04/16/2025
 File Name: main.js
 Description:
 Enhanced JavaScript for the Eyes Unclouded App.
 Includes animated flash fade‑outs, character counters, live form validation,
 and logic to fade splash‑screen text when the intro audio completes.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages
    document.querySelectorAll('.flash-message').forEach(msg => {
      setTimeout(() => {
        msg.style.transition = 'opacity 1s ease, transform 0.5s ease';
        msg.style.opacity = 0;
        msg.style.transform = 'translateY(-10px)';
        setTimeout(() => msg.remove(), 1000);
      }, 4000);
    });
  
    // Character counter for textareas
    const textarea = document.querySelector('#template_body, #message');
    if (textarea) {
      const counter = document.createElement('small');
      counter.classList.add('char-counter');
      textarea.after(counter);
      const update = () => counter.textContent = `${textarea.value.length} characters`;
      textarea.addEventListener('input', update);
      update();
    }
  
    // Live form validation
    const form = document.querySelector('form');
    if (form) {
      form.addEventListener('submit', e => {
        let hasError = false;
        form.querySelectorAll('[required]').forEach(f => {
          if (!f.value.trim()) {
            f.style.borderColor = '#ff5252';
            hasError = true;
          } else {
            f.style.borderColor = '#00ffc3';
          }
        });
        if (hasError) {
          e.preventDefault();
          alert("Please fill out all required fields to continue your path.");
        }
      });
    }
  
    // Fade‑out splash text when intro audio ends
    const audio = document.getElementById('introAudio');
    if (audio) {
      audio.addEventListener('ended', () => {
        // select header, summary paragraph, and button on splash
        document.querySelectorAll('.fade-on-audio').forEach(el => {
          el.classList.add('fade-out');
        });
      });
    }
  });
  