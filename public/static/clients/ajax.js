$.ready(function () {
     $(".item_like").click(function (e) {
        alert('/client/like/');
        e.preventDefault();
        $.ajax({
            url: 'like/',
            type: 'GET',
            dataType: JSON,
            data: {
                'client_id': $("input[type=hidden]").val(),
                'like': $("#number_like").text()
            },
            success: function (data) {
                alert('Voice counted!');
                let count = parseInt($("#number_like").text());
                $("#number_like").html(count+1);
                console.log('good' + data);
            },
            error: function() {
                console.log('error')
            }
        });
     });
});