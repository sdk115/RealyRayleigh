package com.realy.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import com.realy.model.NewsComment;
import com.realy.model.NewsCommentRepository;
import com.realy.model.NewsKeyword;
import com.realy.model.NewsKeywordRepository;

@Controller
public class MainController {
	
	@Autowired // This means to get the bean called userRepository
	private NewsKeywordRepository keywordRespository;
	
	@Autowired
	private NewsCommentRepository newsCommnetRespository;

	@RequestMapping({"/" })
	public String index(Model model) {
		
		model.addAttribute("keywordList", keywordRespository.findAll());
		return "index";
	}
	
	@RequestMapping({"/commentView/{id}" })
	public String comment(Model model, @PathVariable int id) {
		NewsKeyword keyword = keywordRespository.findById(id);
		List<NewsComment> cl1 = newsCommnetRespository.findByKeywordIdAndCategoryIdOrderByRegTimeDesc(id, 1);
		List<NewsComment> cl2 = newsCommnetRespository.findByKeywordIdAndCategoryIdOrderByRegTimeDesc(id, 2);
		int size1 = cl1.size();
		int size2 = cl2.size();
		
		if(size1 > 50)
			cl1 =cl1.subList(0, 50);
		if(size2 > 50)
			cl2 = cl2.subList(0, 50);
		
		model.addAttribute("keyword", keyword.getKeyword());
		model.addAttribute("commentList1", cl1);
		model.addAttribute("size1", size1);
		model.addAttribute("commentList2", cl2);
		model.addAttribute("size2", size2);
		
		return "commentView";
	}
}
