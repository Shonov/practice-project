$().ready( function(){
    $("a#item_like").click(function (e) {
        e.preventDefault();

        let id = $(this).attr("data-id");
        let full_id = '#id_like_' + id;

        console.log(full_id);

        $.ajax({
            url: 'like/',
            type: 'GET',
            dataType: 'json',
            data: {'client_id': id},
            success: function (data) {
                console.log(data['like'])
                // let count = parseInt($(full_id).text());
                $(full_id).html(data['like']);
            }
            // error: function(data, textStatus) {
            //     alert([data.status, textStatus]);
            // },

        });
        return false;
    });
});