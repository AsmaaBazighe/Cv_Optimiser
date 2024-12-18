import os
from dotenv import load_dotenv
from groq import Groq
from google.generativeai import GenerativeModel
import google.generativeai as genai

load_dotenv()

class LLMService:
    def __init__(self):
        # Groq API setup
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Gemini API setup
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = GenerativeModel('gemini-pro')

    def groq_inference(self, system_prompt, user_prompt, model="llama3-8b-8192"):
        """
        Use Groq API for LLM inference
        """
        try:
            completion = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq Inference Error: {e}")
            return "Sorry, I couldn't process your request via Groq."

    def gemini_inference(self, system_prompt, user_prompt):
        """
        Use Google Gemini API for LLM inference
        """
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini Inference Error: {e}")
            return "Sorry, I couldn't process your request via Gemini."

    def analyze_cv_recommendations(self, cv_text, job_description, model='groq'):
        """
        Generate CV recommendations using selected LLM
        """
        system_prompt = """
        You are an expert career coach and CV optimization specialist. 
        Analyze the given CV and job description to provide precise recommendations.
        """
        
        user_prompt = f"""
        CV TEXT: {cv_text}
        
        JOB DESCRIPTION: {job_description}
        
        Please provide the following recommendations:
        1. Skills to add
        2. Skills to remove or de-emphasize
        3. Sections that need improvement
        4. Keywords to include
        5. Potential certifications or training to consider
        """
        
        # Choose LLM based on model parameter
        if model == 'gemini':
            return self.gemini_inference(system_prompt, user_prompt)
        else:
            return self.groq_inference(system_prompt, user_prompt)

    def recommend_learning_resources(self, skill, model='groq'):
        """
        Recommend learning resources for a specific skill
        """
        system_prompt = "You are an educational resource guide specializing in professional skill development."
        
        user_prompt = f"""
        Recommend online learning resources, courses, and certifications 
        for developing proficiency in: {skill}
        
        Include:
        - Free online courses
        - Paid professional courses
        - Certification programs
        - Practice platforms
        - Recommended learning path
        """
        
        # Choose LLM based on model parameter
        if model == 'gemini':
            return self.gemini_inference(system_prompt, user_prompt)
        else:
            return self.groq_inference(system_prompt, user_prompt)