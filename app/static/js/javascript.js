function api_like(n){
    var api_url = "http://127.0.0.1:5000/api/like/"+n;
    console.log(api_url);
    var btn_text = document.getElementById("like");
    var request = new XMLHttpRequest();
    // クライアント側の操作が完了して、HTTPレスポンスが成功したら処理を実行する
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var received_data = JSON.parse(request.responseText);
            btn_text.innerHTML = received_data.like;
        }
    }
    request.open("GET",api_url);
    request.send();
}