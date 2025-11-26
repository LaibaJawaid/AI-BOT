# retrieval.py

import requests
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 

from config import (
    OLLAMA_EMBED_URL, OLLAMA_GENERATE_URL, JOB_LIB_PATH, 
    EMBEDDING_MODEL, LLM_MODEL
)

# --- Global Data Variable ---
DF = None

def load_data():
    """Loads the joblib file into a global DataFrame."""
    global DF
    try:
        DF = joblib.load(JOB_LIB_PATH)
        print("Joblib data loaded successfully.")
        return DF
    except FileNotFoundError:
        print(f"Error: {JOB_LIB_PATH} not found. Please check the file path.")
        DF = None
        return None

# Load data on import
load_data()

# NOTE: create_embedding and inference functions remain the same (with timeout=300)

def create_embedding(input_list):
    """Synchronous function to generate embeddings using Ollama."""
    if not input_list or DF is None:
        return None
    try:
        r = requests.post(OLLAMA_EMBED_URL, json={
            "model": EMBEDDING_MODEL,
            "input": input_list,
        }, timeout=30)
        r.raise_for_status() 
        return r.json()["embeddings"]
    except requests.exceptions.RequestException as e:
        print(f"Error creating embedding: {e}")
        return None

def inference(prompt):
    """Synchronous function to generate response using Ollama."""
    if not OLLAMA_GENERATE_URL:
        return "OLLAMA_URL is not configured."
    try:
        r = requests.post(OLLAMA_GENERATE_URL, json = {
            "model" : LLM_MODEL,
            "prompt": prompt,
            "stream" : False,
            "options": {                # <<< Naya Option
                "num_predict": 400    # <<< Naya Limit
            }
        }, timeout=170) # Ensure this timeout is still 300
        r.raise_for_status()
        response = r.json()
        print(f"--- Ollama Raw Response: {response}") 
        return response.get("response", "Error: No 'response' field in Ollama output.")
    except requests.exceptions.RequestException as e:
        print(f"Error during Ollama inference: {e}")
        return "Sorry, I couldn't connect to the Ollama server or the request timed out."


def perform_rag_retrieval(users_query):
    """Performs the full RAG process (Retrieval + Generation)."""
    
    if DF is None:
        return "The knowledge base is not loaded."

    # 1. Get Embedding
    questions_embedding_list = create_embedding([users_query])
    if questions_embedding_list is None:
        return "Failed to create embedding. Is Ollama running and the bge-m3 model available?"
        
    questions_embedding = questions_embedding_list[0]
    
    # 2. Retrieval 
    stored_embeddings = np.vstack(DF["chunk_embeddings"].values)
    similarities = cosine_similarity(stored_embeddings, [questions_embedding]).flatten()
    
    # Keep retrieval count at 5 for better context coverage
    top_indices = np.argsort(similarities)[-3:][::-1] 
    
    # --- Debugging Output ---
    print(f"\n[RAG Debug] Query: '{users_query}'")
    print(f"Top 3 Similarity Scores: {similarities[top_indices]}")
    
    context_chunks = DF.iloc[top_indices]["content"].values
    context = "\n\n".join(context_chunks)
    print("--- Retrieved Context Chunks ---")
    for i, chunk in enumerate(context_chunks):
        print(f"Chunk {i+1} (Score: {similarities[top_indices][i]:.4f}):\n{chunk[:100]}...\n---")
    # ---------------------------

    # 3. Prompt Construction: IMPROVED INSTRUCTIONS FOR ACCURACY AND DETAIL
   # In retrieval.py, inside the perform_rag_retrieval function (Step 3: Prompt Construction)

    prompt = f"""
    You are an expert on the Azwaj (Wives of the Prophet). Your goal is to be highly accurate.

    **CRITICAL FACTUAL GUARDRAIL:**
    Zaynab Bint Jahsh and Zaynab Bint Khuzaymah are TWO DIFFERENT WIVES.
    Zaynab Bint Khuzaymah is the wife known by the title **"The Mother of the Needy and mother of believers (Umm al-Masakin)"**.
    You MUST use the context to verify facts about the specific wife named in the question.
    
    **CRITICAL FACTUAL CHECK:**
    When answering questions about family relationships (father, husband, daughter, mother, brother), you MUST find the exact term in the context.**DO NOT confuse a wife's father with her husband, or vice versa.
    ** For a question like "Whose daughter was Umm Habibah? Name her father?", you must find the word "father" in the context and provide the name associated with it and Habibah was wife of Prophet nicknamed as Ramlah her mother was Safiyyah bint al-Umawiyyah.

    **Answering Instructions:**
    1.  Use the context below to answer the user's question completely.
    2.  If the question is about a wife with a common name (like Zaynab), you MUST check the full name (Jahsh or Khuzaymah) and use ONLY the facts pertaining to that specific wife. **DO NOT merge their biographies.**
    3.  If the question asks about "Mother of the Needy", you MUST attribute the answer to Zaynab Bint Khuzaymah.
    4.  If the context is insufficient, state the information you *do* have briefly.
    5.  ... (rest of the instructions remain the same) ...

    Context:\n\n{context}\n\nQuestion: {users_query}\n\nAnswer:
    """
    
    # 4. Generation (Inference)
    return inference(prompt)
