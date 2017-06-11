package com.realy.model;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsCommentRepository extends JpaRepository<NewsComment, Long>{
	List<NewsComment> findByKeywordId(int id);
	List<NewsComment> findByKeywordIdAndCategoryId(int kid, int cid);
	List<NewsComment> findByKeywordIdAndCategoryIdOrderByRegTimeDesc(int kid, int cid);
	
}
