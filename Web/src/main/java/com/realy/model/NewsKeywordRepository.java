package com.realy.model;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "keyword", path = "keyword")
public interface NewsKeywordRepository extends JpaRepository<NewsKeyword, Long> {
	NewsKeyword findById(int id);
}
