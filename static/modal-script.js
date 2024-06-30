/* Add this JavaScript to handle the modal */

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('confirmationModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Show the modal
    function showModal() {
        modal.style.display = 'block';
    }

    // Close the modal
    function closeModal() {
        modal.style.display = 'none';
    }

    // Close the modal when the close button is clicked
    closeModalBtn.addEventListener('click', closeModal);

    // Close the modal when clicking outside the modal content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Close the modal when the user presses the Escape key
    window.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });

    // Show the modal after form submission
    showModal();
});
