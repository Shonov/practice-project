$().ready( function(){
    $("a#item_like").click(function (e) {
        e.preventDefault();

        let id = $(this).attr("data-id");
        let full_id = '#id_like_' + id;
        let message = '#message_' + id;

        $.ajax({
            url: 'like/',
            type: 'GET',
            dataType: 'json',
            data: {'client_id': id},
            success: function (data) {
                $(full_id).html(data['like']);
                console.log(data);
                $(message).html(data.message);
            }
            // error: function(data, textStatus) {
            //     alert([data.status, textStatus]);
            // },

        });
        return false;
    });
});
