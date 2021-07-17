function verifyUser(userName, password, onSuccess) {
    $.ajax({
        url: "login",
        data: {
            user_name: userName,
            password: password
        },
        dataType: "json",
        type: "GET",
        success: function(response) {
            onSuccess(response);
        }
    });
}

function signupUser(onSuccess) {
    $.ajax({
        url: "signup",
        contentType: 'application/json',
        dataType: "json",
        type: "POST",
        success: function(response) {
            document.write(response);
        }
    });
}

$("#login").on("click", function() {
    let userName = $("#user-name").val();
    let password = $("#pw").val();
    verifyUser(userName, password, function(message) {
        $("#message").text(message);
    });
});

$("#signup").on("click", function() {
    signupUser(function(message) {
    });
});