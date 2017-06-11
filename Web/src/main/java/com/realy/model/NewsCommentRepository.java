package com.realy.model;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "comment", path = "comment")
public interface NewsCommentRepository extends JpaRepository<NewsComment, Long>{
	List<NewsComment> findByKeywordId(int id);
	List<NewsComment> findByKeywordIdAndCategoryId(int kid, int cid);
	List<NewsComment> findByKeywordIdAndCategoryIdOrderByRegTimeDesc(int kid, int cid);
	Page<NewsComment> findByKeywordIdAndCategoryId(Pageable pageable, int kid, int cid);	
	int countByKeywordId(int id);
	
}
