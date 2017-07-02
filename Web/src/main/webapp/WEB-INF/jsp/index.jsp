<%@page import="java.util.ArrayList"%>
<%@page import="com.realy.model.*"%>
<%@page import="com.fasterxml.jackson.databind.jsonFormatVisitors.JsonArrayFormatVisitor"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<%@ include file="/WEB-INF/jspf/head.jspf"%>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="/js/d3.layout.cloud.js"></script>
<link rel="stylesheet" type="text/css" href="/css/index.css">
</head>

<body>
	<%@ include file="/WEB-INF/jspf/nav.jspf"%>
	<div class="main ui  container">
		<div class="wordcloud-box">
			<div id="wordcloud" class="wordcloud-content"></div>
		</div>

	</div>
</body>

<script>
	var keywordList = new Array();
	<c:forEach items="${keywordList}" var="keyword"  varStatus="status">
	    var keyword = new Object();
	    keyword.text = '${keyword.keyword}';
	    
	    
	    keyword.size = ${ Math.max( 14.4,Math.sqrt(Math.sqrt(countList[status.index]+1))*10 ) }
	    keyword.id = '${keyword.id}'
	    keyword.url = '/commentView/' + '${keyword.id}'
	    keywordList.push(keyword);
	</c:forEach>
	

	var color = d3.scale.linear().domain(
			[ 0, 1, 2, 3, 4, 5, 6, 10, 15, 20, 100 ]).range(
			[ "#333", "#444", "#555", "#666", "#777", "#888", "#999", "#aaa",
					"#bbb", "#ccc", "#ddd", "#eee" ]);
	
	d3.layout.cloud().size([ 900, 750 ]).words(keywordList).rotate(0)
			.fontSize(function(d) {
				return d.size;
			}).on("end", draw).start();
	
	function draw(words) {
		var width = $('#wordcloud').width();
		var height = 700;
		d3.select("#wordcloud").append("svg").attr("width", 1080).attr("height",
				700).attr("class", "wordcloud").append("g")
		// without the transform, words words would get cutoff to the left and top, they would
		// appear outside of the SVG area
		.attr("transform", "translate(400,300)").selectAll("text").data(words)
				.enter().append("text").style("font-size", function(d) {
					return d.size + "px";
				}).style("fill", function(d, i) {
					return color(i);
				}).attr(
						"transform",
						function(d) {
							return "translate(" + [ d.x, d.y ] + ")rotate("
									+ d.rotate + ")";
						}).text(function(d) {
					return d.text;
				}).on("click", function (d, i){location.href = d.url;}) 
		}
   
</script>

</html>