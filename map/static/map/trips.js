const deleteTripModal = document.getElementById('deleteTripModal')
deleteTripModal.addEventListener('show.bs.modal', event => {
  // Button that triggered the modal
  const button = event.relatedTarget
  // Extract info from data-bs-* attributes
  const trip_destination = button.getAttribute('data-bs-trip')
  const trip_id = button.getAttribute('data-bs-trip-id')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  document.getElementById('trip-destination').innerHTML = trip_destination;
  document.getElementById('delete-trip-button').onclick = () => {
    deleteTrip(trip_id, trip_destination);
    bootstrap.Modal.getInstance(document.getElementById('deleteTripModal')).hide();
  }
})


function deleteTrip(trip_id, trip_destination) {
  fetch('/api/trip/' + trip_id, {
    method: 'DELETE'
  })
  .then(response => response.json())
  .then(result => {
    showAlert(result.message, 'danger');
    document.getElementById(`accordion-item-${trip_id}`).remove();
  });
}


const editTripModal = document.getElementById('editTripModal')
editTripModal.addEventListener('show.bs.modal', event => {

  // Button that triggered the modal
  const button = event.relatedTarget

  // Extract info from data-bs-* attributes
  const trip_id = button.getAttribute('data-bs-trip-id')

  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  fetch('/api/trip/' + trip_id, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    // Update the modal's content.
    document.getElementById('edit-location').value = data.location;
    document.getElementById('edit-state').value = data.state;
    document.getElementById('edit-date1').value = data.date1;
    document.getElementById('edit-date2').value = data.date2;
    document.getElementById('edit-description').value = data.description;

    document.getElementById('reset-trip-button').onclick = () => {
      document.getElementById('edit-location').value = data.location;
      document.getElementById('edit-state').value = data.state;
      document.getElementById('edit-date1').value = data.date1;
      document.getElementById('edit-date2').value = data.date2;
      document.getElementById('edit-description').value = data.description;
    }

    document.getElementById('edit-trip-button').onclick = () => {
      editTrip(data.id);
      bootstrap.Modal.getInstance(document.getElementById('editTripModal')).hide();
    }

  })
});


function editTrip(trip_id) {
  fetch('/api/trip/' + trip_id, {
    method: 'PUT',
    body: JSON.stringify({
      'location': document.getElementById('edit-location').value,
      'state': document.getElementById('edit-state').value,
      'date1': document.getElementById('edit-date1').value,
      'date2': document.getElementById('edit-date2').value,
      'description': document.getElementById('edit-description').value
    })
  })
  .then(response => response.json())
  .then(result => {
    state = document.getElementById('edit-state');

    date1 = '';
    date2 = '';

    if (document.getElementById('edit-date1').value != '') {
      date1 = new Date(Date.parse(document.getElementById('edit-date1').value)).toLocaleDateString('en-us', { timeZone: 'UTC', year: 'numeric', month: 'short', day: 'numeric'});
    }

    if (document.getElementById('edit-date2').value != '') {
      date2 = new Date(Date.parse(document.getElementById('edit-date2').value)).toLocaleDateString('en-us', { timeZone: 'UTC', year: 'numeric', month: 'short', day: 'numeric'});
    }

    dates = date1;
    if (date2 != '' ) {
      dates += ' &ndash; ' + date2;
    }

    document.getElementById('trip-' + trip_id + '-location').innerHTML = document.getElementById('edit-location').value;
    document.getElementById('trip-' + trip_id + '-state').innerHTML = state.options[state.selectedIndex].text;
    document.getElementById('trip-' + trip_id + '-flag').src = 'static/map/flags/' + state.value + '.svg';

    document.getElementById('trip-' + trip_id + '-dates').innerHTML = dates;

    document.getElementById('trip-' + trip_id + '-description').innerHTML = document.getElementById('edit-description').value;

    showAlert(result.message, 'success');
  })

}