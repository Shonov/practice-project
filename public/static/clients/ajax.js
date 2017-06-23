$().ready(function () {

    $("p#item_like").click(function (e) {
        e.preventDefault();

        let id = $(this).attr("data-id");
        let full_id = `#id_like_${id}`;

        $.ajax({
            url: 'like/',
            type: 'GET',
            dataType: 'json',
            data: {'client_id': id},
            success: (data) => {
                $(full_id).html(data['like']);
                if (data.message) {
                    toastr.error(data.message);
                }

            },
            error: (data, textStatus) => {
                alert(data.status, textStatus)
            }
        });
        return false;
    });
});
