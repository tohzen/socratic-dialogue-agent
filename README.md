# Socratic Dialogue Agent

A full-stack AI application designed to engage users in philosophical dialogue. The agent uses a Retrieval-Augmented Generation (RAG) pipeline to provide answers sourced from a curated library of philosophical texts and then poses a new, Socratic question to stimulate deeper thought.

![Socratic Agent Demo](demo.gif)
*(You will replace this line after creating a GIF of the app in action!)*

---

## Features

- **Socratic Dialogue:** This agent doesn't just answer questions, it encourages further reflection by asking a relevant, open-ended questions in return.
- **Retrieval-Augmented Generation (RAG):** Maintaining a healthy chunk size is important as it provides answers grounded in a specific knowledge base of philosophical texts, reducing hallucination.
- **Source Citation:** Every answer is accompanied by the source text name and page number, used for its generation, ensuring transparency and allowing for deeper user research.
- **Full-Stack Application:** A complete application with a Python backend and a web-based user interface.

---

## Tech Stack

- **Backend:** Python, FastAPI, LangChain, OpenAI API
- **Vector Database:** FAISS (in-memory)
- **Frontend:** HTML, Bootstrap 5, vanilla JavaScript
- **Server:** Uvicorn

---

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.\.venv\Scripts\Activate.ps1`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    - Create a file named `.env` in the root of the project.
    - Add your OpenAI API key to the file:
      ```
      OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
      ```

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

6.  Open your browser and navigate to `http://127.0.0.1:8000`.