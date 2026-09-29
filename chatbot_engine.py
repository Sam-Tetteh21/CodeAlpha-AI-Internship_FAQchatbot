"""
chatbot_engine.py
------------------
This module contains the "brain" of the FAQ chatbot:
1. Text preprocessing (cleaning) using NLTK
2. Matching a user's question to the closest FAQ using TF-IDF + cosine similarity

Concepts explained (since this is new territory):

- Tokenizing: splitting a sentence into individual words.
  "How do I register?" -> ["how", "do", "i", "register"]

- Stopwords: common words like "the", "is", "do", "how" that carry little
  meaning on their own. Removing them helps the matching focus on the
  important words.

- Lemmatizing: reducing a word to its base/dictionary form.
  "registering", "registered", "registers" -> "register"
  This helps match "How do I register" with "registering for courses"
  even though the exact word form differs.

- TF-IDF (Term Frequency - Inverse Document Frequency): a way of turning
  text into numbers (a vector) so a computer can compare sentences
  mathematically. Words that are rare across all FAQs get more weight,
  because rare words are more useful for telling questions apart.

- Cosine similarity: a score between 0 and 1 that measures how similar
  two vectors (sentences) are. 1 = identical meaning-direction, 0 = totally
  unrelated. We use this to find which FAQ question is closest to what
  the user typed.
"""

import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def ensure_nltk_data():
    """Download the small NLTK datasets we need, only if missing."""
    required = [
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
    ]
    for path, package in required:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)


ensure_nltk_data()

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """
    Turn raw text into a cleaned, space-joined string of lemmatized,
    non-stopword tokens. E.g.:
    "How do I register for courses?" -> "register course"
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    cleaned_tokens = [
        _lemmatizer.lemmatize(token)
        for token in tokens
        if token not in _stop_words and token.isalpha()
    ]
    return " ".join(cleaned_tokens)


class FAQChatbot:
    """
    Wraps a list of FAQ dicts ({"question": ..., "answer": ...}) and
    answers new questions by finding the most similar FAQ question.
    """

    def __init__(self, faqs: list, similarity_threshold: float = 0.25):
        self.faqs = faqs
        self.similarity_threshold = similarity_threshold

        # Preprocess every FAQ question once, up front.
        self.cleaned_questions = [clean_text(faq["question"]) for faq in faqs]

        # Fit a TF-IDF vectorizer on the FAQ questions. "Fitting" means
        # the vectorizer learns the vocabulary (all unique words) from
        # these questions so it can turn any new sentence into a
        # comparable vector later.
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(self.cleaned_questions)

    def get_response(self, user_question: str):
        """
        Returns (answer_text, matched_faq_question, similarity_score).
        If nothing matches well enough, returns a fallback message.
        """
        cleaned_input = clean_text(user_question)

        if not cleaned_input.strip():
            return (
                "Could you rephrase that? I didn't catch any keywords to work with.",
                None,
                0.0,
            )

        # Turn the user's question into a vector using the SAME
        # vocabulary learned from the FAQs.
        user_vector = self.vectorizer.transform([cleaned_input])

        # Compare the user's vector against every FAQ vector at once.
        similarities = cosine_similarity(user_vector, self.faq_vectors)[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]

        if best_score < self.similarity_threshold:
            return (
                "I'm not sure about that one. Could you rephrase, or contact "
                "the Student Affairs office for help with this?",
                None,
                float(best_score),
            )

        matched_question = self.faqs[best_index]["question"]
        answer = self.faqs[best_index]["answer"]
        return answer, matched_question, float(best_score)
