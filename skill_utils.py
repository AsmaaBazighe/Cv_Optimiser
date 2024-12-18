import re
from typing import List

def extract_skill_from_query(query: str) -> str:
    """
    Extract the specific skill from a user's query about learning resources
    
    Args:
        query (str): User's input query
    
    Returns:
        str: Extracted skill name
    """
    # List of common phrasings to remove
    skill_markers = [
        "learning resources for", 
        "how to learn", 
        "learn", 
        "resources for", 
        "courses in", 
        "training for"
    ]
    
    # Lowercase the query and remove skill markers
    cleaned_query = query.lower()
    for marker in skill_markers:
        cleaned_query = cleaned_query.replace(marker, '').strip()
    
    # Use regex to extract potential skill
    skill_match = re.findall(r'\b[a-zA-Z\s#\+\-]+\b', cleaned_query)
    
    # Return the first match, or a default if no match
    return skill_match[0].strip() if skill_match else "general skills"

def get_skill_recommendations(current_skills: List[str]) -> List[dict]:
    """
    Generate skill recommendations based on current skills
    
    Args:
        current_skills (List[str]): List of skills the user currently has
    
    Returns:
        List[dict]: Recommended skills with additional context
    """
    # Predefined skill clusters and recommendations
    skill_recommendations = {
        "programming": {
            "web_dev": ["React", "Node.js", "TypeScript", "GraphQL"],
            "cloud": ["AWS", "Docker", "Kubernetes", "Azure"],
            "data_science": ["Python", "Machine Learning", "TensorFlow", "PyTorch"]
        },
        "data_analysis": {
            "tools": ["Power BI", "Tableau", "SQL", "Excel Advanced"],
            "languages": ["R", "Python", "SAS"]
        },
        "soft_skills": {
            "leadership": ["Project Management", "Team Communication", "Strategic Planning"],
            "professional_dev": ["Negotiation", "Public Speaking", "Cross-functional Collaboration"]
        }
    }
    
    recommended_skills = []
    
    # Simple recommendation logic
    for category, skill_groups in skill_recommendations.items():
        for group, skills in skill_groups.items():
            for skill in skills:
                # Skip skills user already has
                if skill.lower() not in [s.lower() for s in current_skills]:
                    recommended_skills.append({
                        "skill": skill,
                        "category": category,
                        "group": group,
                        "rationale": f"Complementary skill to enhance your {category} expertise"
                    })
    
    # Sort recommendations by relevance (you could implement more sophisticated ranking)
    recommended_skills.sort(key=lambda x: len(x['skill']), reverse=True)
    
    return recommended_skills[:5]  # Return top 5 recommendations