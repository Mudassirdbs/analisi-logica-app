# Analisi Logica Online

## Overview
A web application for automatic Italian grammatical analysis that identifies subject, predicate, and grammatical complements using Natural Language Processing (spaCy with Italian model). Features include speech input via microphone and dark/light mode toggle.

**Created:** October 18, 2025  
**Status:** Fully functional MVP

## Features
- ✅ Text input for Italian sentences
- ✅ Speech recognition using Web Speech API (microphone input)
- ✅ Automatic grammatical analysis using spaCy NLP (it_core_news_sm model)
- ✅ Identification of subject (soggetto), predicate (predicato), and complements (complementi)
- ✅ Clear results display with detailed tables
- ✅ Educational guide explaining each complement type
- ✅ Pre-loaded example sentences for quick testing
- ✅ Dark/light mode toggle with persistent user preference
- ✅ Fully responsive Italian-language interface

## Project Architecture

### Backend (Python Flask)
- **app.py**: Main Flask application with NLP analysis endpoint
  - `/` - Serves the main HTML page
  - `/analyze` - POST endpoint that analyzes Italian sentences using spaCy
  - Identifies: subjects, predicates, objects, and various complements

### Frontend
- **templates/index.html**: Main application interface with semantic HTML
- **static/style.css**: Responsive styling with CSS variables for theming
- **static/script.js**: Client-side logic for:
  - Speech recognition (Web Speech API)
  - Analysis requests to Flask backend
  - Results display and formatting
  - Theme switching (dark/light mode)
  - Example sentence loading

## Technical Stack
- **Backend**: Python 3.11, Flask, Flask-CORS, spaCy
- **NLP Model**: it_core_news_sm (Italian language model)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Speech Input**: Web Speech API (browser-native)

## Italian Grammar Analysis
The app identifies:
- **Soggetto** (Subject): Who/what performs the action
- **Predicato** (Predicate): The verb expressing the action
- **Complemento Oggetto** (Direct Object): Answers "Chi? Che cosa?"
- **Complemento di Termine** (Indirect Object): Answers "A chi? A che cosa?"
- **Complemento di Specificazione** (Specification): Answers "Di chi? Di che cosa?"
- **Complemento di Luogo** (Place): Answers "Dove? Da dove? Verso dove?"
- **Complemento di Compagnia** (Company): Answers "Con chi?"
- **Complemento Avverbiale** (Adverbial): Modifies the verb

## Recent Changes
- **Oct 18, 2025**: Enhanced grammatical analysis to match educational standards
  - Added ATTRIBUTO detection (adjectives with adverb modifiers)
  - Added CONGIUNZIONE detection (conjunctions)
  - Improved COMPLEMENTO DI TERMINE detection (including "loro")
  - Added COMPLEMENTO OGGETTO PARTITIVO detection (partitive articles)
  - Added conjoined objects detection
  - Created "Altri Elementi" section in results display
  - Fixed error handling to preserve DOM structure
  - Improved complement detection using proper preposition analysis
  
- **Oct 18, 2025**: Initial project creation
  - Installed Python 3.11 and required dependencies
  - Downloaded spaCy Italian model (it_core_news_sm)
  - Created Flask backend with grammatical analysis logic
  - Built responsive frontend with speech input
  - Implemented dark/light theme toggle
  - Added example sentences and educational guide

## Usage
1. Enter an Italian sentence in the text field (or click microphone to speak)
2. Click "Analizza" to perform grammatical analysis
3. View results showing subject, predicate, and complements
4. Check the detailed token analysis table
5. Use example sentences for quick testing
6. Toggle between dark/light mode for comfortable viewing

## Development Notes
- The Flask server runs on port 5000
- Speech recognition requires HTTPS or localhost
- Browser must support Web Speech API (Chrome, Edge recommended)
- spaCy model provides automatic dependency parsing for Italian
