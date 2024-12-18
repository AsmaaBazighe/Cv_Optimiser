from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

class KnowledgeGraph:
    def __init__(self, uri=None, username=None, password=None):
        """
        Initialize Neo4j connection
        You can pass credentials or use environment variables
        """
        load_dotenv()  # Load environment variables
        
        uri = uri or os.getenv('NEO4J_URI')
        username = username or os.getenv('NEO4J_USERNAME')
        password = password or os.getenv('NEO4J_PASSWORD')
        
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def get_job_recommendations(self, skills: List[str]) -> List[Dict[str, Any]]:
        """
        Recommend jobs based on user's current skills
        
        Args:
            skills (List[str]): List of skills the user possesses
        
        Returns:
            List[Dict]: Recommended jobs with matching skills and details
        """
        with self.driver.session() as session:
            query = """
            MATCH (j:Job)
            OPTIONAL MATCH (j)-[:USES]->(p:Programming)
            OPTIONAL MATCH (j)-[:HAS_SKILL]->(s:TechnicalSkill)
            WHERE p.name IN $skills OR s.name IN $skills
            WITH j, 
                 COLLECT(DISTINCT p.name) AS matching_programming_skills,
                 COLLECT(DISTINCT s.name) AS matching_technical_skills
            RETURN 
                j.name AS job_title, 
                matching_programming_skills, 
                matching_technical_skills,
                SIZE(matching_programming_skills) + SIZE(matching_technical_skills) AS match_score
            ORDER BY match_score DESC
            LIMIT 5
            """
            result = session.run(query, skills=skills)
            return [
                {
                    "job_title": record["job_title"],
                    "matching_programming_skills": record["matching_programming_skills"],
                    "matching_technical_skills": record["matching_technical_skills"],
                    "match_score": record["match_score"]
                } for record in result
            ]

    def get_skill_recommendations(self, current_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Recommend skills based on job market trends and current skills
        
        Args:
            current_skills (List[str]): List of skills the user currently has
        
        Returns:
            List[Dict]: Recommended skills with context
        """
        with self.driver.session() as session:
            query = """
            UNWIND $current_skills AS current_skill
            MATCH (j:Job)-[:USES|:HAS_SKILL]->(s:TechnicalSkill)
            WHERE s.name <> current_skill
            WITH s.name AS recommended_skill, 
                 COUNT(DISTINCT j) AS job_count, 
                 COLLECT(DISTINCT j.name) AS related_jobs
            ORDER BY job_count DESC
            LIMIT 10
            RETURN 
                recommended_skill, 
                job_count, 
                related_jobs
            """
            result = session.run(query, current_skills=current_skills)
            return [
                {
                    "skill": record["recommended_skill"],
                    "job_count": record["job_count"],
                    "related_jobs": record["related_jobs"]
                } for record in result
            ]

    def get_learning_resources(self, skill: str) -> List[Dict[str, str]]:
        """
        Find learning resources and certifications for a specific skill
        
        Args:
            skill (str): Skill to find resources for
        
        Returns:
            List[Dict]: Learning resources and certifications
        """
        with self.driver.session() as session:
            query = """
            MATCH (j:Job)-[:REQUIRES]->(c:Certification)
            WHERE c.name CONTAINS $skill
            RETURN 
                c.name AS certification, 
                j.name AS related_job
            LIMIT 5
            """
            result = session.run(query, skill=skill)
            return [
                {
                    "certification": record["certification"],
                    "related_job": record["related_job"]
                } for record in result
            ]

    def get_project_recommendations(self, skills: List[str]) -> List[Dict[str, Any]]:
        """
        Recommend projects based on user's skills
        
        Args:
            skills (List[str]): List of skills the user possesses
        
        Returns:
            List[Dict]: Recommended projects with details
        """
        with self.driver.session() as session:
            query = """
            MATCH (p:Project)-[:ASSOCIATED_WITH]->(j:Job)
            OPTIONAL MATCH (j)-[:USES|:HAS_SKILL]->(s:TechnicalSkill)
            WHERE s.name IN $skills
            RETURN 
                p.title AS project_title, 
                p.domain AS domain, 
                p.description AS description,
                COLLECT(DISTINCT s.name) AS matching_skills
            LIMIT 5
            """
            result = session.run(query, skills=skills)
            return [
                {
                    "project_title": record["project_title"],
                    "domain": record["domain"],
                    "description": record["description"],
                    "matching_skills": record["matching_skills"]
                } for record in result
            ]