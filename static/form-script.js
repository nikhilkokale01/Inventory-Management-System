function submitForm(formId) {
    const form = document.getElementById(formId);
    const confirmationMessage = document.getElementById('confirmationMessage');

    // Make an AJAX request to submit the form data
    fetch(form.action, {
        method: form.method,
        body: new FormData(form),
    })
    .then(response => response.json())  // Assuming the server responds with JSON
    .then(data => {
        // Display the confirmation message
        confirmationMessage.style.display = 'block';
        setTimeout(() => {
            // Hide the confirmation message after a few seconds
            confirmationMessage.style.display = 'none';
        }, 3000);  // Adjust the time as needed
    })
    .catch(error => console.error('Error submitting form:', error));
}
