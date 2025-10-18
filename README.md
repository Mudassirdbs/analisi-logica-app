# Analisi Logica Online

An Italian grammatical analysis web application that uses Natural Language Processing (spaCy) to identify subjects, predicates, and complements in Italian sentences.

## Features

- 🎯 Automatic identification of grammatical elements:
  - **Soggetto** (Subject)
  - **Predicato Verbale** (Predicate)
  - **Complementi** (Complements): Oggetto, Termine, Specificazione, Luogo, Compagnia, Avverbiale
  - **Altri Elementi**: Attributi, Congiunzioni
- 🎤 Speech recognition for voice input
- 📱 Responsive design
- 🇮🇹 Full Italian language support

## Tech Stack

- **Backend**: Flask (Python)
- **NLP**: spaCy with Italian model (it_core_news_sm)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Deployment**: Vercel

## Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL)

### Manual Deployment

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Production Deploy**:
   ```bash
   vercel --prod
   ```

### GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Click "Deploy"

That's it! Vercel will automatically detect the Flask app and deploy it.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy Italian model
python -m spacy download it_core_news_sm

# Run the app
python api/index.py
```

## Project Structure

```
.
├── api/
│   ├── index.py          # Flask application
│   ├── templates/        # HTML templates
│   └── static/          # CSS and JavaScript
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── README.md
```

## Usage

1. Enter an Italian sentence in the text field
2. Or click the microphone button to speak
3. Click "Analizza" to perform grammatical analysis
4. View the results showing all grammatical elements

## Example Sentences

- Il gatto mangia il pesce sul tavolo.
- Maria legge un libro interessante in biblioteca.
- Marcella ha dato loro istruzioni molto precise e degli utili consigli.

## License

MIT
