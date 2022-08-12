let i = 0;
var tbodyRef = document.getElementById('orderTable').getElementsByTagName('tbody')[0];

function rowTemplate(i) {
  return `<tr data-index=${i}>
      <td>${i}</td>
      <td><input placeholder="Select" list="menu" name="item${i}" class="item" required></td>
      <td><input placeholder="0" type="number" name="quantity${i}" class="quantity" min="0" required></td>
      <td><i class="fa fa-times-circle" style="font-size: 15px; color: red;" onclick="removeRow(${i})"></i></td>
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




