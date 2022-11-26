const visitedStateCSS = 'fill: #0d6efd !important;';
updateStates();

var detailsBox = document.getElementById('info-box');

document.addEventListener('mouseover', function (e) {
  if (e.target.tagName == 'path') {
    var content = e.target.dataset.name;
    detailsBox.innerHTML = content;
    detailsBox.style.opacity = "100%";
  }
  else {
    detailsBox.style.opacity = "0%";
  }
});

document.addEventListener('click', function (e) {
  if (e.target.tagName == 'path') {
    window.open(`/state/${e.target.dataset.id}`,'_self',false)
  }
});

window.onmousemove = function (e) {
  var x = e.clientX,
      y = e.clientY;
  detailsBox.style.top = (y + 20) + 'px';
  detailsBox.style.left = (x) + 'px';
};


// Fetch the list of state visited by the logged user and color them
function updateStates() {
  fetch('api/states')
  .then(response => response.json())
  .then(states => {
      if (states.error == null) {
        states.forEach((state) => {
          document.getElementById(state).style.cssText = visitedStateCSS;
        });
      }
  });
}
