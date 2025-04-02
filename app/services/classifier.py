import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from ..data.database import Database
from ..utils.generate_response import generate_response

df = pd.read_csv('app/data/emails.csv')
emails = df['text']
labels = df['label']

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)
model = MultinomialNB()
model.fit(X, labels)

db = Database()

def classify_email(email):
    X_test = vectorizer.transform([email])
    prediction = model.predict(X_test)
    classification = "important" if prediction[0] == 1 else "not important"
    response = generate_response(email, classification)
    db.save_email(email, classification, response)
    return {
        "classification": classification,
        "response": response
    }