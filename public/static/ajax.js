/**
 * Created by vitaly on 15.06.17.
 */
$.ready(function () {
     $("#item_like").on('click', function() {
        $.ajax({
            url: 'index',
            type: 'GET',
            dataType: JSON,
            data: {
                'like': $("#number_like").val()
            },
            success: function (data) {
                console.log('good')
                alert('All ready!' + data)
            }
        });
     })

});