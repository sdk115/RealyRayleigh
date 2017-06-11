<%@page import="java.util.ArrayList"%>
<%@page import="com.realy.model.*"%>
<%@page import="com.fasterxml.jackson.databind.jsonFormatVisitors.JsonArrayFormatVisitor"%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<%@ include file="/WEB-INF/jspf/head.jspf"%>
<link rel="stylesheet" type="text/css" href="/css/commentView.css">
<script type="text/javascript" src="http://mbostock.github.com/d3/d3.js?2.1.3"></script>
<script type="text/javascript" src="http://mbostock.github.com/d3/d3.geom.js?2.1.3"></script>
<script type="text/javascript" src="http://mbostock.github.com/d3/d3.layout.js?2.1.3"></script>
</head>

<body>
	<%@ include file="/WEB-INF/jspf/nav.jspf"%>
	<div class="main ui container">
		<div class="ui grid">

			<div class="four wide column ">
				<div>
					<h2 id ="title"><${keyword}></h2> 
				</div>
				
				<div id="slice-area"></div>
				
				<h4 id= "static-text">
					찬성 : <fmt:formatNumber value="${ size1 / (size1+size2) * 100}" type="number" pattern="#.#"/>% /
					반대 : <fmt:formatNumber value="${ size2 / (size1+size2) * 100}" type="number" pattern="#.#"/>%
				</h4>
				
			</div>
			<div class="six wide column ">
				<h3>찬성 - ${size1}건</h3>
				<c:forEach var="comment" items="${commentList1}">
					<div class="ui segment">
						<span class="ui  floated left text comment-nick">${comment.userName}</span>
						<span class="ui  floated  righttext comment-reg">${comment.regTime}</span>
						 
						<div class="ui divider "></div>
						${comment.contents}
					</div>
				</c:forEach>

			</div>

			<div class="six wide column ">
				<h3>반대 - ${size2}건</h3>
				<c:forEach var="comment" items="${commentList2}">
					<div class="ui segment">
						<span class="ui  floated left text comment-nick">${comment.userName}</span>
						<span class="ui  floated  righttext comment-reg">${comment.regTime}</span>
						<div class="ui divider "></div>
						${comment.contents}
					</div>
				</c:forEach>
			</div>
		</div>
	</div>
</body>

<script type="text/javascript">
    var w = 400,                        //width
    h = 300,                            //height
    r = 130,                            //radius
    color = d3.scale.ordinal([0,1]).range(["#1E90FF","#B22222"]);
    

    data = [{"label":"찬성", "value":${size1}}, 
            {"label":"반대", "value":${size2}}];
    
    var vis = d3.select("#slice-area")
        .append("svg:svg")              //create the SVG element inside the <body>
        .data([data])                   //associate our data with the document
            .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
            .attr("height", h)
        .append("svg:g")                //make a group to hold our pie chart
            .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
        .outerRadius(r);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
        .value(function(d) { return d.value; });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties) 
        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
            .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
                .attr("class", "slice");    //allow us to style things in the slices (like text)

        arcs.append("svg:path")
                .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
                .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

        arcs.append("svg:text")                                     //add a label to each slice
                .attr("transform", function(d) {                    //set the label's origin to the center of the arc
                //we have to make sure to set these before calling arc.centroid
                d.innerRadius = 0;
                d.outerRadius = r;
                return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
            })
            .attr("text-anchor", "middle")                          //center the text on it's origin
            .text(function(d, i) { return data[i].label; });        //get the label from our original data array
        
    </script>

</html>