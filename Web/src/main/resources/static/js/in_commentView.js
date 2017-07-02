/**
 * 
 */

function postComment(){
//	alert("hi")
	
	var content = $('#commentContent').val();
	var checked = $('input:radio[name="agree"]:checked').val();
	var userId = $('#userId').val();
	
	if( checked == undefined){
		alert("찬성 혹은 반대를 체크해주세요.");
	}
	else if(content == ""){
		alert("내용을 입력해주세요.");
	}
	else if(userId == ""){
		alert("로그인을 해주세요.")
	}
	else{
		$('#commentForm').submit()
	}
}