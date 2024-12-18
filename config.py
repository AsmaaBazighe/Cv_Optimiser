import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

# Free embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Directories
FAISS_INDEXER_DIR = os.path.join(CURRENT_DIR, "indexer_ckpt")
TEMP_DATA_DIR = os.path.join(CURRENT_DIR, "temp_data")

# CV Analysis Features
SUMMARY_FEATURES = [
    "technical skills", 
    "education background", 
    "relevant experience", 
    "certifications", 
    "projects"
]