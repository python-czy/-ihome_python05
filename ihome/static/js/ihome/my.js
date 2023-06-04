// js 读取cookie的方法
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击退出按钮时执行的函数	
function logout() {
	$.ajax({
		url:"/api/v1.0/session",
		type:"delete",
		headers:{
			"X-CSRFToken":getCookie("csrf_token")
		},
		dataType:"json",
		success:function(resp){
			if ("0" == resp.errno){
				location.href = "index.html";
			}
	    }
    })
}

// $(document).ready(function() {
// 	$.get("/api/v1.0/user/profile", function(data){
// 		$("#user-avatar").attr("src", data.data.avatar)
// 		$("#user-name").html(data.data.name),
// 		$("#user-mobile").html(data.data.mobile)
// 	})
// })
$(document).ready(function() {
	$.get("/api/v1.0/user/profile", function(resp){
		//用户未登录
		if (resp.errno == "4101"){
			location.herf = "/login.html"
		}
		// 查询到了用户的信息
		else if (resp.errno == "0"){
			$("#user-name").html(resp.data.name);
			$("#user-mobile").html(resp.data.mobile);
			if (resp.data.avatar){
				$("#user-avatar").attr("src", resp.data.avatar)
			}
		}
	}, "json");
})