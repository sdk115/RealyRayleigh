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
		List<NewsComment> cl1 = newsCommnetRespository.findByKeywordIdAndCategoryId(id, 1);
		List<NewsComment> cl2 = newsCommnetRespository.findByKeywordIdAndCategoryId(id, 2);
		model.addAttribute("keyword", keyword.getKeyword());
		model.addAttribute("commentList1", cl1);
		model.addAttribute("size1", cl1.size());
		model.addAttribute("commentList2", cl2);
		model.addAttribute("size2", cl2.size());
		
		return "commentView";
	}
}
