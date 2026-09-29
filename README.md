# CodeAlpha_FAQChatbot

A chat-style FAQ chatbot for university student services, built during my **CodeAlpha Artificial Intelligence Internship** (Task 2).

Ask it about course registration, exams, fees, IDs, transcripts, and more — it uses NLP techniques to understand your question and match it to the most relevant answer, even if you don't phrase it exactly like the FAQ.

## 🌍 Live Demo
👉 [Try it live here](PASTE_YOUR_STREAMLIT_APP_LINK_HERE)

## 🎥 Video Demo
[LinkedIn video link here]

## ✨ Features
- Chat-style interface (like messaging apps) built with Streamlit's chat components
- Understands question variations, not just exact matches, using NLP preprocessing
- Shows a confidence score and which FAQ was matched, for transparency
- Politely says "I'm not sure" instead of guessing when no FAQ is a good match

## 🛠️ Tech Stack & How Matching Works
- **Python 3**
- **[Streamlit](https://streamlit.io/)** — chat UI (`st.chat_message`, `st.chat_input`)
- **[NLTK](https://www.nltk.org/)** — text preprocessing: tokenizing, stopword removal, lemmatizing
- **[scikit-learn](https://scikit-learn.org/)** — TF-IDF vectorization + cosine similarity for matching

**In plain terms:** every FAQ question and the user's typed question are cleaned (lowercased, punctuation removed, common words like "the"/"is" removed, words reduced to their base form), then converted into numeric vectors using TF-IDF. Cosine similarity measures how close the user's question is to each FAQ question mathematically, and the closest match's answer is returned. If nothing is close enough (below a similarity threshold), the bot admits it doesn't know rather than giving a wrong answer.

## 📂 Project Structure
```
CodeAlpha_FAQChatbot/
├── app.py               # Streamlit chat UI
├── chatbot_engine.py     # Text preprocessing + TF-IDF/cosine similarity matching
├── faqs.py                # The FAQ question/answer dataset
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 How to Run Locally

### One-click Windows startup

From the project folder, run either of these:

```powershell
./run_app.ps1
```

or just double-click:

```text
run_app.bat
```

This creates a virtual environment the first time, installs dependencies once, and starts the app. On later days, you can run the same command again without repeating the full setup.

### Manual setup

1. Clone this repository
   ```bash
   git clone https://github.com/<your-username>/CodeAlpha_FAQChatbot.git
   cd CodeAlpha_FAQChatbot
   ```

2. (Optional) create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app
   ```bash
   streamlit run app.py
   ```
   The first run will automatically download a few small NLTK language datasets (tokenizer, stopwords, lemmatizer) — this needs an internet connection and only happens once.

5. Your browser will open at `http://localhost:8501`. Type a question in the chat box at the bottom.

## 📝 Customizing the FAQs
Open `faqs.py` and edit the `FAQS` list — each entry is a `{"question": ..., "answer": ...}` pair. Add as many as you like; the chatbot automatically re-learns the vocabulary from whatever is in that file.

## 📌 About the Internship
This project was built as part of the **CodeAlpha Artificial Intelligence Internship**.

- Website: [www.codealpha.tech](https://www.codealpha.tech)
- Task: Chatbot for FAQs

## 👤 Author
[Your Name] — BSc. Information Technology Education
