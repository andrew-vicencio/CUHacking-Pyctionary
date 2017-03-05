function getPoints() {
    w;
    
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/getpts",
        success: function(data) {
            $("#x_pos").text(data.x)
            $("#y_pos").text(data.y)
            $("#hwall").text(data.w)
            w = data.w
        }
    });
    
    if(w == 1)
        background.src="/getmaze"
}

function go() {
    setInterval(getPoints, 100)
}
