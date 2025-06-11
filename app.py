from flask import Flask, render_template, request, jsonify
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Training data
training_data = {
    "weather": [
        "what's the weather like?",
        "is it going to rain?",
        "do I need an umbrella?",
        "how hot is it today?",
        "tell me the weather"
    ],
    "smalltalk": [
        "hello",
        "hi",
        "how are you?",
        "good morning",
        "good evening",
        "tell me a joke",
        "say something fun"
    ],
    "facts": [
        "who is the president of the united states?",
        "what is the capital of france?",
        "how many continents are there?",
        "tell me a fact about space",
        "what's the tallest mountain"
    ]
}

# Possible responses for each intent
responses = {
    "weather": [
        "I'm not sure of the exact weather, but it's always a great day to code!",
        "It's always sunny in the command line!",
        "Looks like perfect coding weather." 
    ],
    "smalltalk": [
        "Hello! How can I assist you today?",
        "Hi there! Ask me anything.",
        "I'm doing great, thanks for asking!"
    ],
    "facts": [
        "The Earth revolves around the Sun once every 365 days.",
        "The capital of France is Paris.",
        "Mount Everest is the tallest mountain above sea level." 
    ],
    "fallback": [
        "I'm sorry, I don't understand.",
        "Could you rephrase that?",
        "I'm not sure how to respond to that." 
    ]
}

# Prepare training set
sentences = []
labels = []
for intent, examples in training_data.items():
    for sentence in examples:
        sentences.append(sentence)
        labels.append(intent)

# Vectorizer and classifier
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)
classifier = LogisticRegression(max_iter=1000)
classifier.fit(X, labels)


def predict_intent(text: str) -> str:
    vec = vectorizer.transform([text])
    pred = classifier.predict(vec)[0]
    return pred


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"response": random.choice(responses["fallback"])})

    intent = predict_intent(user_message.lower())
    answer_pool = responses.get(intent, responses["fallback"])
    return jsonify({"response": random.choice(answer_pool)})


if __name__ == '__main__':
    app.run(debug=True)
