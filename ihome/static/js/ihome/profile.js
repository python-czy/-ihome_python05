function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
	$("#form-avatar").submit(function(e){
		// 阻止表单的默认行为
		e.preventDefault();
		// 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
		$(this).ajaxSubmit({
			url:"/api/v1.0/user/avatar",
			type:"post",
			dataType:"json",
			headers:{
				"X-CSRFToken":getCookie("csrf_token")
			},
			success:function(resp){
				if (resp.errno == "0"){
					// 上传成功
					var avatarUrl = resp.data.avatar_url;
					$("#user-avatar").attr("src", avatarUrl);
				}
				else{
					alert(resp.errmsg);
				}
			}
		})
	})
	$("#form-name").submit(function(e){
		// 阻止表单的默认行为
		e.preventDefault();
		// 获取参数
		var name = $("#user-name").val();
		if (!name){
			alert("请填写用户名！");
			return
		}
		$.ajax({
			url:"/api/v1.0/user/name",
			type:"PUT",
			data:JSON.stringify({name: name}),
			contentType:"application/json",
			dataType:"json",
			headers:{
				"X-CSRFToken":getCookie("csrf_token")
			},
			success:function(data){
				if (data.errno == "0"){
					// 上传成功
					$(".error-msg").hide();
					showSuccessMsg()
				}
				else if(data.errno == "4001"){
					$(".error-msg").show();
				}
				else if(data.errno == "4101"){
					location.href = "/login,html"
				}
			}
		})
	})
	
})
