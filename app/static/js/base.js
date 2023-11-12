/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggleButton() {
  var dropdown = document.getElementById("dropdownMenu");
  dropdown.style.display = (dropdown.style.display == 'block') ? 'none' : 'block';
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdownContent");
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}