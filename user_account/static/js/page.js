function follow_this(e){
	// 关注用户
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '{% url "wb:follow" %}?uid={{ wb_user.id }}', true);
	xhr.onreadystatechange=function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			e.setAttribute('onclick', 'unfollow_this(this)');
			e.setAttribute('class', 'btn btn-success btn-lg');
			e.innerText = '已关注';
		};
	};
	xhr.send();
};

function unfollow_this(e){
	// 解除关注
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '{% url "wb:unfollow" %}?uid={{ wb_user.id }}', true);
	xhr.onreadystatechange=function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			e.setAttribute('onclick', 'follow_this(this)');
			e.setAttribute('class', 'btn btn-primary btn-lg');
			e.innerText = '关注';
		};
	};
	xhr.send();	
}

function forward_this(wid){
	document.getElementById('forward_weibo').setAttribute('value', wid);
}
function comm_cancel(e){
	// 取消评论
	var comm = e.parentElement.parentElement.parentElement;
	comm.parentElement.removeChild(comm);
};

function comm_this(e, wid){
	// 向表格填入 weibo.id
	var ee = e.parentElement.nextElementSibling,
		dd = document.createElement('div');
	dd.setAttribute('class', 'panel panel-default container-fluid');
	dd.innerHTML = `\
		<div class="panel-heading row">\
			<span class="col-sm-1">评论：</span>\
			<span class="col-sm-1 pull-right"><input class="btn btn-success" type="submit" form="comm_form" onclick="comm_post(this)" value='发送'></span>\
			<span class="col-sm-1 pull-right"><a class="btn btn-danger" onclick="comm_cancel(this)">取消</a></span>\
		</div>\
		<div class="panel-body">\
			<form id="comm_form" method="POST" action="{% url "wb:comment" %}">\
				{% csrf_token %}\
				<textarea name="msg" class="form-control" placeholder="上限500字符" rows=8 maxlength=500></textarea>\
				<input class="hidden" name="wid" value="` + wid + `">\
			</form>\
		</div>`
	ee.appendChild(dd);
};

function comm_post(ee){
	// 发送评论
	document.getElementById('comm_form').onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest();
		xhr.open("POST", f.action, true);
		xhr.onreadystatechange=function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				var dataReply = xhr.responseText,
					para = ee.parentElement.parentElement.parentElement,
					newBox = document.createElement('div');
				para.innerHTML = dataReply;
			};
		};
		xhr.send(formData);
	};
};