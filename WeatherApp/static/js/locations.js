$(".locations").sortable({
        update: function(event, data) {
            var locationName = data.item.context.children[1].children[0].children[0].children[0].textContent;
            var locations = [];
            var newIndex;

            $('.locations article').each(function () {
                locations.push($(this).context.children[1].children[0].children[0].children[0].innerText);
            });

            for (i = 0; i < locations.length; i++) {
                if (locations[i] == locationName) {
                    newIndex = i;
                    break;
                }
            }

            $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "locationSort",
             'locationName': locationName,
             'newIndex': newIndex},
			function (data) {
                if (data.result == "Fail")
                    alert(data.appStatus);
			});
        }
});
$(".locations").disableSelection();


countLocations();

// request weather for new locations after entering the list name
$('.add-location').focus();
$('.add-location').on('keypress',function (event) {
    event.preventDefault;
    if (event.which == 13) {
        if($(this).val() != ''){
            var location = $(this).val();
            createLocation(location);
        }
    }
});

// delete a Location
$('.locations').on('click','.remove-location',function(){
    removeItem(this);
});

// count TodoLists
function countLocations(){
    var count = $(".locations article").length;
    $('.count-locations').html(count);
}

function createLocation(text){
    $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "Create",
             'locationName': text},
			function (data) {
                if (data.result == "Fail")
                {
                    alert(data.appStatus);
                    $('.add-location').val('');
                }
                else
                {
                    location.reload();
                    $('.add-location').val('');
                    countLocations();
                }
			});
}

function removeItem(element){
    var removedItem = element.parentNode.parentNode.children[1].children[0].children[0].children[0].textContent;
    $.post(window.location.pathname,
            {   csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'submit': "Delete",
                'locationName': removedItem},
                function (data) {
                    if (data.result == "Fail")
                        alert(data.appStatus);
                    else
                    {
                        $(element).parent().parent().remove();
                        countLocations();
                    }
            }
          );
}

