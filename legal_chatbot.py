# legal_chatbot.py

import json
import random
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required nltk packages
nltk.download('punkt')
nltk.download('wordnet')

# Preprocessing
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Load Legal FAQs
with open('legal_faq.json', 'r') as file:
    faq = json.load(file)

questions = faq['questions']
answers = faq['answers']

# Preprocess all questions
cleaned_questions = [clean_text(q) for q in questions]

# Initialize Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(cleaned_questions)

# Chatbot Logic
def get_response(user_input):
    user_input_clean = clean_text(user_input)
    user_vec = vectorizer.transform([user_input_clean])
    
    similarities = cosine_similarity(user_vec, X)
    max_sim_idx = similarities.argmax()
    max_sim_score = similarities[0, max_sim_idx]
    
    if max_sim_score < 0.3:  # Threshold for understanding
        return "I'm sorry, I couldn't understand your query. Please consult a legal professional."
    else:
        return answers[max_sim_idx]

# Main Chat Loop
def chat():
    print("LegalBot: Hello! I can answer your basic legal questions. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("LegalBot: Thank you for using LegalBot. Goodbye!")
            break
        response = get_response(user_input)
        print(f"LegalBot: {response}")

if __name__ == "__main__":
    chat()
