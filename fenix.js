const notesToggle = document.getElementById('notes-toggle');
notesToggle.addEventListener('change', () => {
  document.body.classList.toggle('hide-notes', !notesToggle.checked);
});
