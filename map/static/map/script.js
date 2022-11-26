function resetTrip() {
    document.getElementById('location').value = '';
    document.getElementById('state').value = 'State (required)';
    document.getElementById('date1').value = '';
    document.getElementById('date2').value = '';
    document.getElementById('description').value = '';
}


function addTrip() {
    let trip_location = document.getElementById('location').value;
    let trip_state = document.getElementById('state').value;
    let trip_date1 = document.getElementById('date1').value;
    let trip_date2 = document.getElementById('date2').value;
    let trip_description = document.getElementById('description').value;

    // Add trip using API
    fetch('/api/trip', {
        method: 'POST',
        body: JSON.stringify({
            location: trip_location,
            state: trip_state,
            date1: trip_date1,
            date2: trip_date2,
            description: trip_description
        })
    })
    .then(response => response.json())
    .then(result => {
        var tripModal = bootstrap.Modal.getInstance(document.getElementById('addTripModal'));
        tripModal.hide();
        document.getElementById('addTripModal').addEventListener('hidden.bs.modal', event => {
            showAlert(result.message, 'success');
        }, {once : true})
        resetTrip();
        updateStates();
    });
}

function showAlert(message, type) {
    const alertDiv = document.getElementById('alert');

    const alert = (message, type) => {
        const wrapper = document.createElement('div')
        wrapper.innerHTML = [
          `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
          `   <div>${message}</div>`,
          '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
          '</div>'
        ].join('')

        alertDiv.append(wrapper)
    }

    alert(message, type);

}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))