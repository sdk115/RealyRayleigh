package com.realy.model;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;


public interface NewsKeywordRepository extends JpaRepository<NewsKeyword, Long> {
	NewsKeyword findById(int id);
}
