function api_like(n){
    var api_url = "http://127.0.0.1:5000/api/like/"+n;
    var btn_text = document.getElementById("like-" + n);
    var like_icon = document.getElementById("like-icon");
    var request = new XMLHttpRequest();
    // クライアント側の操作が完了して、HTTPレスポンスが成功したら処理を実行する
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var received_data = JSON.parse(request.responseText);
            btn_text.innerHTML = received_data.like;
            if(received_data.like_is == 1){
                like_icon.style.color = "#a9a9a9";
            }else{
                like_icon.style.color = "#1DA1F2";
            }
        }
    }
    request.open("GET",api_url);
    request.send();
}