package com.realy.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.connect.Connection;
import org.springframework.social.connect.ConnectionData;
import org.springframework.social.connect.ConnectionRepository;
import org.springframework.social.facebook.api.Facebook;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import com.realy.model.NewsComment;
import com.realy.model.NewsCommentRepository;
import com.realy.model.NewsKeyword;
import com.realy.model.NewsKeywordRepository;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Controller
public class MainController {
	
	@Autowired // This means to get the bean called userRepository
	private NewsKeywordRepository keywordRespository;
	
	@Autowired
	private NewsCommentRepository newsCommnetRespository;
	
	@Autowired
	private ConnectionRepository connectionRepository;
	
	@RequestMapping({"/" })
	public String index(Model model) {
		User user = getConnect();
		
		List<NewsKeyword> keywordList = keywordRespository.findAll();
		
		int sum = 0;
		
		List<Integer> countList = new ArrayList<Integer>();
		for (int i = 0 ; i<keywordList.size(); i++)
		{
			int id =keywordList.get(i).getId();
			int count = newsCommnetRespository.countByKeywordId(id);
			sum+=count;
			countList.add(count);			
		}
		
		model.addAttribute("user", user);
		model.addAttribute("keywordList", keywordList);
		model.addAttribute("keywordCount", keywordList.size());
		model.addAttribute("commentCount", sum);
		model.addAttribute("countList", countList);
	
		return "index";
	}
	
	@RequestMapping({"/commentView/{id}" })
	public String comment(Model model, @PathVariable int id) {
		NewsKeyword keyword = keywordRespository.findById(id);
		List<NewsComment> cl1 = newsCommnetRespository.findByKeywordIdAndCategoryIdOrderByRegTimeDesc(id, 1);
		List<NewsComment> cl2 = newsCommnetRespository.findByKeywordIdAndCategoryIdOrderByRegTimeDesc(id, 2);
		int size1 = cl1.size();
		int size2 = cl2.size();
		model.addAttribute("keywordCount", keywordRespository.findAll().size());
		model.addAttribute("commentCount", newsCommnetRespository.findAll().size());
		if(size1 > 50)
			cl1 =cl1.subList(0, 50);
		if(size2 > 50)
			cl2 = cl2.subList(0, 50);
		
		model.addAttribute("keywordId",id);
		model.addAttribute("keyword", keyword.getKeyword());
		model.addAttribute("commentList1", cl1);
		model.addAttribute("size1", size1);
		model.addAttribute("commentList2", cl2);
		model.addAttribute("size2", size2);
		
		User user = getConnect();
		model.addAttribute("user", user);
		
		
		return "commentView";
	}
	
	private User getConnect() {
		Connection<Facebook> connection = connectionRepository.findPrimaryConnection(Facebook.class);
		if (connection == null) {
			return null;
		}
		ConnectionData data = connection.createData();
		return new User(data.getProviderUserId(), data.getDisplayName());
	}
	
	public static class User {
		private String providerUserId;
		private String displayName;
		public User(String providerUserId2, String displayName2) {
			// TODO Auto-generated constructor stub
			providerUserId = providerUserId2;
			displayName = displayName2;
		}
		
		public String getProviderUserId() {
			return providerUserId;
		}
		public void setProviderUserId(String providerUserId) {
			this.providerUserId = providerUserId;
		}
		public String getDisplayName() {
			return displayName;
		}
		public void setDisplayName(String displayName) {
			this.displayName = displayName;
		}
	}
}
