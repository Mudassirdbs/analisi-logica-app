from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
from spacy.cli import download as spacy_download
from pathlib import Path

# --- Model Loading Logic ---
# Vercel provides a writable /tmp directory. We'll store the model there.
MODEL_NAME = "it_core_news_sm"
MODEL_PATH = Path(f"/tmp/{MODEL_NAME}")
nlp = None # Initialize nlp as None

def load_spacy_model():
    """Checks if the model is downloaded, downloads it if not, and then loads it."""
    global nlp
    if not MODEL_PATH.exists():
        print(f"Model '{MODEL_NAME}' not found in /tmp. Downloading...")
        # Download the model to the /tmp directory
        spacy_download(MODEL_NAME, "--direct", "-q", "-d", "/tmp")
        print("Download complete.")
    
    # Load the model from the /tmp directory
    nlp = spacy.load(MODEL_PATH)
    print("spaCy model loaded successfully.")

# Load the model when the application starts
load_spacy_model()
# --- End of Model Loading Logic ---


app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if not request.json or 'sentence' not in request.json:
        return jsonify({'error': 'Nessuna frase fornita.'}), 400

    sentence = request.json['sentence']
    
    if not nlp:
        return jsonify({'error': 'Modello NLP non caricato.'}), 500
        
    doc = nlp(sentence)

    # (Your existing analysis logic goes here. No changes needed to this part.)
    # ... for example:
    analysis_result = {
        'soggetto': [],
        'predicato': [],
        'complementi': [],
        'altri_elementi': [],
        'tokens': []
    }
    
    for token in doc:
        analysis_result['tokens'].append({
            'text': token.text,
            'pos': token.pos_,
            'dep': token.dep_,
            'head': token.head.text
        })
        if "subj" in token.dep_:
            analysis_result['soggetto'].append(token.text)
        elif token.pos_ == "VERB" or token.pos_ == "AUX":
            analysis_result['predicato'].append(token.text)
        # Add the rest of your complement detection logic here...

    return jsonify(analysis_result)

# This is only for local testing, Vercel uses its own server.
if __name__ == '__main__':
    app.run(debug=True, port=5000)
