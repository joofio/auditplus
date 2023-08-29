$(document).ready(function () {
    $('#Maintable').DataTable();
});

$(document).ready(function () {

    $('.js-data-example-ajax').select2({
        ajax: {
            url: '/select2search',
            dataType: 'json',
            data: function (params) {
                var query = {
                    search: params.term,
                    ontology: ontologyButton.checked

                }
                console.log(ontologyButton.checked);
                return query;
            }
        },
        placeholder: 'Search for a keyword',
        minimumInputLength: 1,
        tags: true
    })
});


function createresult(doc_id, query_id, decision) {
    console.log(doc_id, decision)
    $.ajax({
        type: 'POST',
        url: '/decision',
        data: { "doc_id": doc_id, "decision": decision, "query_id": query_id },
        success: function (msg) {
            alert(msg);
        }
    });

}

// When the user clicks on <div>, open the popup
function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
  }
