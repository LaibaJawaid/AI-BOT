m                                                                          aaaaaaaaaaaaaasiiiiiiiiiiiiiiiiiiiiidddddddddddddddddddddddddddddddddddddddddddddx# 🌺 RAG-Based — Prophet's Wives Great Lives — Guidance Bot

A highly accurate **Retrieval-Augmented Islamic Guidance Bot** that answers questions about the **Mothers of the Believers (Azwāj al-Mu’minīn)** using a custom knowledge base, semantic search, and local LLM generation.
Built with **Python, Ollama, discord.py, and BGE-M3 embeddings**.

---

## ✨ Key Features

* **📚 Authentic Islamic Knowledge**

  * Answers drawn strictly from your curated biography dataset.
  * Focuses on the life stories, virtues, and history of the Prophet’s Wives (RA).

* **🔍 Retrieval-Augmented Generation (RAG)**

  * Semantic search using **BGE-M3** embeddings.
  * Top-3 context retrieval for high accuracy.

* **🛡 Strong Accuracy Guardrails**

  * Prevents mixing of similar names (e.g., two Zaynabs).
  * Enforces “father/husband/daughter” relationship correctness.
  * No hallucinated information — only context-based answers.

* **🤖 Discord Bot Integration**

  * Use command:

    ```
    !azwaj <your question>
    ```
  * Auto-typing indicator & clean formatting.

* **📝 Long Message Handling**

  * Splits responses automatically if they exceed Discord's 2000-character limit.

* **⚡ Local & Fast**

  * Fully offline using **Ollama** for embeddings + LLM inference.

---

## 🧱 Tech Stack & Components

| Component                | Technology        | Purpose                        |
| ------------------------ | ----------------- | ------------------------------ |
| **Python**               | 3.10+             | Main backend logic             |
| **discord.py**           | Bot framework     | Discord command handling       |
| **Ollama**               | Local LLM runtime | Embedding & generation         |
| **BGE-M3**               | Embedding model   | High-accuracy semantic vectors |
| **Llama3.2 / Phi3-Mini** | LLM               | Contextual response generation |
| **Joblib + Pandas**      | Vector store      | Stores chunks & embeddings     |
| **Cosine Similarity**    | sklearn           | Ranking chunks by relevance    |

---

Here you go!
**A perfect Languages & Tools block** for your **RAG-Based Prophet’s Wives Guidance Bot** — showing **only the technologies you actually used**.

Just **copy–paste** this directly into your GitHub README.
(Exactly same style as the example you gave.)

---

### 🖥️ Languages & Tools

<p>
  <!-- Programming Language -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

  <!-- RAG & ML Tools -->

  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/BGE--M3-6C63FF?style=for-the-badge&logo=ai&logoColor=white" />
  <img src="https://img.shields.io/badge/LLaMA_3.2-7D4698?style=for-the-badge&logo=meta&logoColor=white" />

  <!-- Python Libraries -->

  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/pandas-130654?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/joblib-1D6F42?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/requests-005571?style=for-the-badge&logo=python&logoColor=white" />

  <!-- Discord -->

  <img src="https://img.shields.io/badge/discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white" />

  <!-- General Dev Tools -->

  <img src="https://img.shields.io/badge/Git-F05033?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white" />
</p>

---

## 📂 Project Structure

```
📦 Prophet-Wives-RAG-Bot
│
├── bot.py                     # Discord bot logic & message splitting
├── retrieval.py               # Retrieval + LLM generation pipeline
├── config.py                  # Environment variables & API URLs
│
├── newJoblib.joblib           # Final knowledge base with embeddings
├── embed_chunks_bge.json      # Embedding metadata (JSON)
│
├── semantic_chunks.json       # Cleaned book text (chunked)
├── CHUNK.py                   # PDF → semantic chunks processing
├── newembeds.py               # Embedding generation script
│
├── prophet’s wives.pdf        # Source material
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation
```

---

## 🚀 How It Works

1. **Semantic Chunking**
   * `CHUNK.py` extracts, cleans, and splits text from the PDF.

2. **Embedding Generation**
   * `newembeds.py` converts chunks to embeddings using **BGE-M3**.

3. **Vector Store**
   * Saved into `newJoblib.joblib` with:
     * chunk text
     * aliases
     * embeddings

4. **RAG Pipeline** (`retrieval.py`)
   * User query → embedding
   * Compare with stored embeddings
   * Retrieve top-3 chunks
   * Build safe prompt with guardrails
   * Send to Llama3.2/Phi3 via Ollama

5. **Discord Interaction** (`bot.py`)
   * User sends `!azwaj <question>`
   * Bot shows typing
   * Runs RAG pipeline
   * Splits final reply if >2000 chars

---

## 🛠️ Installation

### 1️⃣ Install Python Requirements

```bash
pip install -r requirements.txt
```

### 2️⃣ Install Ollama Models

```bash
ollama pull bge-m3
ollama pull llama3.2
# optional
ollama pull phi3:mini
```

### 3️⃣ Set Up Environment Variables

Create **.env**:

```
DISCORD_TOKEN=YOUR_BOT_TOKEN
OLLAMA_URL=http://localhost:11434/api/generate
```

### 4️⃣ Run the Bot

```bash
python bot.py
```

---

## 💬 Usage Example

On Discord:

```
!azwaj who was the Mother of the Needy?
```

```
!azwaj what was the lineage of Umm Habibah?
```

---

## 🛡 Built-in Accuracy Guardrails

The bot enforces:

* Do **not** mix:

  * Zaynab bint Jahsh
  * Zaynab bint Khuzaymah
* Only answer using provided context.
* Explicit father/mother/husband checks.
* No invented information.
* State clearly when context is insufficient.

---

## ⭐ Support

If this project helps you, ⭐ **star the repo** on GitHub!

---
