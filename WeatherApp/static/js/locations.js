$(".locations").sortable({
        update: function(event, data) {
            var currentItems = "";

            $('.locations article').each(function () {
                currentItems += $(this).context.children[1].children[0].children[0].children[0].textContent + ',';
            });

            var orderList = JSON.stringify(currentItems.slice(0,-1));

            $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "LocationSort",
             'orderList': orderList},
			function (data) {
                if (data.result == "Fail")
                    alert(data.appStatus);
			});

        }
});
$(".locations").disableSelection();

countLocations();

// Weather information gets refreshed for every 2 hours for all current set of locations
setTimeout(refreshWeather, 7200000);

// adding a new location to get its weather data
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

// deleting a location
$('.locations').on('click','.remove-location',function(){
    removeItem(this);
});

// delete all current locations
$("#removeAll").click(function(){
    removeAll();
});


// count current set of locations
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

function removeAll(){
    $.post(window.location.pathname,
        { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'submit': "Delete All"
        },
        function (data) {
            if (data.result == "Fail")
                    alert(data.appStatus);
            else
            {
                $('.locations article').remove();
                countLocations();
                $('.add-location').val('');
            }
        }

        );
}


function refreshWeather(){
    $.post(window.location.pathname,
            { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
             'submit': "Refresh"},
			function (data) {
                if (data.result == "Fail")
                    alert(data.appStatus);
                else
                    location.reload();
			});
    setTimeout(refreshWeather, 7200000);
}

