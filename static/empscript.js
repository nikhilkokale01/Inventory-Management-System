document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.sidebar a');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            // Prevent the default behavior of the link
            event.preventDefault();

            // Remove the 'active' class from all links
            links.forEach(l => l.classList.remove('active'));

            // Add the 'active' class to the clicked link
            link.classList.add('active');

            // Fetch and display the content for the clicked link
            const url = link.getAttribute('href');
            fetchContent(url);
        });
    });

    // Function to fetch and display content
    function fetchContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, 'text/html');

                // Update the content area with the new content
                const contentContainer = document.querySelector('.container');
                contentContainer.innerHTML = newDocument.querySelector('.container').innerHTML;
            })
            .catch(error => console.error('Error fetching content:', error));
    }


});

// empscript.js
// empscript.js

function markAsDelivered(orderId) {
    // Send an AJAX request to update the delivery status
    fetch(`/mark_as_delivered/${orderId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If the update is successful, update the UI or perform any necessary actions
            alert('Order marked as delivered successfully.');
            // You may want to update the UI here, for example, change the button to 'Delivered'
            // or remove the button.
        } else {
            alert('Failed to mark order as delivered.');
        }
    })
    .catch(error => console.error('Error marking order as delivered:', error));
}

