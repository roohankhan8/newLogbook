function saveAndRedirect(nextPageUrl) {
    // Save data using AJAX
    var formData = new FormData(document.getElementById('myForm'));
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save-data/', true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Data saved successfully.');
            // Redirect the user to the next page
            window.location.href = nextPageUrl;
        } else {
            console.log('Failed to save data.');
        }
    };
    xhr.send(formData);
}
