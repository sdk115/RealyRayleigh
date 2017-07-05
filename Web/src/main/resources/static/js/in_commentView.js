/**
 * 
 */

function postComment() {
	// alert("hi")

	var content = $('#commentContent').val();
	var checked = $('input:radio[name="agree"]:checked').val();
	var userId = $('#userId').val();
	if (userId == "") {
		warning("로그인을 해주세요.")
	} else if (checked == undefined) {
		warning("찬성 혹은 반대를 체크해주세요.");
	} else if (content == "") {
		warning("내용을 입력해주세요.");
	} else {
		$('#commentForm').submit()
	}
}

function warning(text) {
	$.uiAlert({
		textHead : '오류 발생!', // header
		text : text, // Text
		bgcolor : '#F2711C', // background-color
		textcolor : '#fff', // color
		position : 'top-center',// position . top And bottom || left / center /
		// right
		icon : 'warning sign', // icon in semantic-UI
		time : 1.3, // time
	});

}