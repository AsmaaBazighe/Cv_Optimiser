import streamlit as st
import re
from hf_inference import LLMService
from neo4j_knowledge_graph import KnowledgeGraph
from utilities import extract_pdf_text
from typing import List

class CVOptimizer:
    def __init__(self):
        # Initialize services
        self.llm_service = LLMService()
        self.knowledge_graph = KnowledgeGraph()

    def extract_skills_from_cv(self, cv_text: str) -> List[str]:
        """
        Extract skills from CV text using NLP
        
        Args:
            cv_text (str): Full CV text
        
        Returns:
            List[str]: Extracted skills
        """
        # Basic skill extraction (you might want to improve this with more advanced NLP)
        skills_patterns = [
            r'\b(Python|Java|C\+\+|SQL|R|Machine Learning|Data Analysis)\b',
            r'\b(TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy)\b',
            r'\b(AWS|Azure|Cloud|Docker|Kubernetes)\b'
        ]
        
        skills = []
        for pattern in skills_patterns:
            skills.extend(re.findall(pattern, cv_text, re.IGNORECASE))
        
        return list(set(skills))

    def optimize_cv(self, cv_text: str, job_description: str) -> dict:
        """
        Optimize CV using knowledge graph and LLM
        
        Args:
            cv_text (str): Full CV text
            job_description (str): Job description text
        
        Returns:
            dict: CV optimization recommendations
        """
        # Extract skills from CV
        current_skills = self.extract_skills_from_cv(cv_text)
        
        # Get job recommendations based on current skills
        job_recommendations = self.knowledge_graph.get_job_recommendations(current_skills)
        
        # Get skill recommendations
        skill_recommendations = self.knowledge_graph.get_skill_recommendations(current_skills)
        
        # Use LLM to generate detailed optimization advice
        llm_optimization = self.llm_service.analyze_cv_recommendations(
            cv_text, 
            job_description
        )
        
        return {
            "current_skills": current_skills,
            "job_recommendations": job_recommendations,
            "skill_recommendations": skill_recommendations,
            "llm_optimization": llm_optimization
        }

def main():
    st.title("AI CV Optimizer & Career Coach")
    
    # Initialize CV Optimizer
    cv_optimizer = CVOptimizer()
    
    # Sidebar for file uploads
    with st.sidebar:
        st.header("Upload Documents")
        cv_file = st.file_uploader("Upload your CV", type=['pdf'])
        job_description_file = st.file_uploader("Upload Job Description", type=['pdf', 'txt'])
    
    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat input
    if prompt := st.chat_input("How can I help you optimize your career?"):
        # Process user query
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Different query handling
            if "job recommendations" in prompt.lower():
                if cv_file:
                    # Extract CV skills and get job recommendations
                    cv_text = extract_pdf_text(cv_file)
                    current_skills = cv_optimizer.extract_skills_from_cv(cv_text)
                    job_recommendations = cv_optimizer.knowledge_graph.get_job_recommendations(current_skills)
                    
                    st.write("Job Recommendations:")
                    for job in job_recommendations:
                        st.write(f"**{job['job_title']}**")
                        st.write(f"Matching Skills: {job['matching_programming_skills'] + job['matching_technical_skills']}")
                else:
                    st.write("Please upload your CV first.")
            
            elif "learn" in prompt.lower():
                # Extract skill from query
                skill = re.findall(r'\b(Python|Java|Machine Learning|Data Science)\b', prompt, re.IGNORECASE)
                if skill:
                    learning_resources = cv_optimizer.knowledge_graph.get_learning_resources(skill[0])
                    st.write(f"Learning Resources for {skill[0]}:")
                    for resource in learning_resources:
                        st.write(f"- {resource['certification']} (Related Job: {resource['related_job']})")
            
            elif cv_file and job_description_file:
                # Full CV optimization
                cv_text = extract_pdf_text(cv_file)
                job_description = extract_pdf_text(job_description_file)
                
                optimization_result = cv_optimizer.optimize_cv(cv_text, job_description)
                
                st.write("CV Optimization Recommendations:")
                st.write("Current Skills:", optimization_result['current_skills'])
                
                st.write("\nJob Recommendations:")
                for job in optimization_result['job_recommendations']:
                    st.write(f"- **{job['job_title']}**")
                
                st.write("\nSkill Recommendations:")
                for skill in optimization_result['skill_recommendations']:
                    st.write(f"- **{skill['skill']}** (Found in {skill['job_count']} jobs)")
                
                st.write("\nDetailed Optimization Advice:")
                st.write(optimization_result['llm_optimization'])
            
            else:
                st.write("Please upload your CV and job description.")

if __name__ == "__main__":
    main()