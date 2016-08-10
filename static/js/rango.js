$(document).ready(function(){
    $('#about-btn').click(function(){
        alert("你是个王八蛋!");
        $("#about-btn").addClass('btn btn-primary');

        var msgStr = $('#msg').html();
        msgStr += ' Append Later!';
        $('#msg').html(msgStr);
    });

});

// 下面的做法在家里的也适合
// $('#about-btn').click(function(){
//     alert("你是个王八蛋!");
//     $("#about-btn").addClass('btn btn-primary');
//
//     var msgStr = $('#msg').html();
//     msgStr += ' Append Later!';
//     $('#msg').html(msgStr);
// });
