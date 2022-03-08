function searchFilter() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("dataTable");
  tr = table.getElementsByTagName("tr");
  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td");
    txtValue = '';
    for (j=0; j<td.length; j++) {
      txtValue += td[j].textContent || td[j].innerText;
    }

    if (txtValue.toUpperCase().indexOf(filter) > -1) {
    tr[i].style.display = "";
    } else {
    tr[i].style.display = "none";
    }
  }
}

