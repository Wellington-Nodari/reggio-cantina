let i = 0;
var tbodyRef = document.getElementById('orderTable').getElementsByTagName('tbody')[0];

function rowTemplate(i) {
  return `<tr data-index=${i}>
      <td><input placeholder="Select" list="menu" name="item${i}" class="item" required></td>
      <td><input placeholder="0" type="number" name="quantity${i}" class="quantity" min="0" required></td>
      <td><i class="fa fa-times-circle" style="font-size: 12px; color: #B22222;" onclick="removeRow(${i})"></i></td>
    </tr>`
}

for (i = 0; i < 1; i ++) {
  $(tbodyRef).append(rowTemplate(i));
}

function removeRow(i) {
  $(tbodyRef).find(`tr[data-index='${i}']`).remove();
  i--; return i;
}

function addRow() {
  $(tbodyRef).append(rowTemplate(i));
  i++;
}


// To modal window

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("toModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function(e) {
  modal.style.display = "none";
  e.preventDefault();
  return false;
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


//      <td>${i}</td>