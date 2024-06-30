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
                const contentContainer = document.querySelector('.content');
                contentContainer.innerHTML = newDocument.querySelector('.content').innerHTML;
            })
            .catch(error => console.error('Error fetching content:', error));
    }


});
// ... (previous script content) ...
    function showForm(formName) {
        const formsContainer = document.getElementById('forms-container');
        fetch(`/${formName}`)
            .then(response => response.text())
            .then(html => {
                formsContainer.innerHTML = html;
            })
            .catch(error => console.error('Error fetching form:', error));
    }

    function submitForm(formName) {
        const form = document.getElementById(`${formName}-form`);
        const formsContainer = document.getElementById('forms-container');

        fetch(`/${formName}`, {
            method: 'POST',
            body: new FormData(form),
        })
            .then(response => response.text())
            .then(html => {
                formsContainer.innerHTML = html;
            })
            .catch(error => console.error('Error submitting form:', error));
    }

// ... (previous script content) ...

function showView(viewName) {
    const viewContainer = document.getElementById('view-container');
    fetch(`/${viewName}`)
        .then(response => response.text())
        .then(html => {
            viewContainer.innerHTML = html;
        })
        .catch(error => console.error('Error fetching view:', error));
}
// ... (previous script content) ...


function showEditForm(formName, itemId) {
    const editContainer = document.getElementById('edit-container');
    fetch(`/${formName}/${itemId}`)
        .then(response => response.text())
        .then(html => {
            editContainer.innerHTML = html;
        })
        .catch(error => console.error(`Error fetching edit form for ${formName}:`, error));
}


function hideEditForm() {
    const editContainer = document.getElementById('edit-container');
    editContainer.innerHTML = ''; // Clear the content
}


    function deleteItem(tableName, itemId) {
        fetch(`/${tableName}/delete/${itemId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Reload the view after deletion (you might consider updating the view without a full page reload)
            showView('view_' + tableName);
        })
        .catch(error => console.error(`Error deleting ${tableName}:`, error));
    }
 function updateEntity(event, entityId, entityName) {
    event.preventDefault();  // Prevent the default form submission

    // Collect form data
    const formData = new FormData(event.target);

    // Send an AJAX request
    fetch(`/update_${entityName}/${entityId}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data (if needed)
        console.log(data);

        // After updating, fetch and update the corresponding section
//        showView(`view_${entityName}`);
    })
    .catch(error => {
        // Handle errors
        console.error(`Error updating ${entityName}:`, error);
    });
}
