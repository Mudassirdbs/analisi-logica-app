from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)

nlp = spacy.load('it_core_news_sm')

def analyze_sentence(text):
    doc = nlp(text)
    
    results = {
        'tokens': [],
        'subject': [],
        'predicate': [],
        'complements': [],
        'other_elements': []
    }
    
    for token in doc:
        token_info = {
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'head': token.head.text
        }
        results['tokens'].append(token_info)
        
        if token.dep_ == 'nsubj' or token.dep_ == 'nsubj:pass':
            results['subject'].append({
                'text': token.text,
                'type': 'Soggetto',
                'description': 'Indica la persona, animale o cosa che compie o subisce l\'azione'
            })
        
        if token.pos_ == 'VERB' or token.pos_ == 'AUX':
            verb_form = 'Verbo ausiliare' if token.pos_ == 'AUX' else 'Verbo'
            results['predicate'].append({
                'text': token.text,
                'type': 'Predicato Verbale',
                'description': f'{token.text} - {verb_form} ({token.lemma_})'
            })
        
        if token.dep_ == 'obj':
            has_partitive = False
            for child in token.children:
                if child.dep_ == 'case' and child.text.lower() in ['degli', 'delle', 'dei']:
                    has_partitive = True
                    break
            
            if has_partitive:
                adjectives = [child.text for child in token.children if child.dep_ == 'amod']
                obj_text = token.text
                if adjectives:
                    obj_text = ' '.join(adjectives) + ' ' + obj_text
                
                results['complements'].append({
                    'text': obj_text,
                    'type': 'Complemento Oggetto Partitivo',
                    'description': 'Complemento oggetto preceduto da articolo partitivo'
                })
            else:
                results['complements'].append({
                    'text': token.text,
                    'type': 'Complemento Oggetto',
                    'description': 'Risponde alla domanda "Chi? Che cosa?"'
                })
        
        elif token.dep_ == 'conj':
            if token.head.dep_ == 'obj':
                has_partitive = False
                for child in token.children:
                    if child.dep_ == 'case' and child.text.lower() in ['degli', 'delle', 'dei']:
                        has_partitive = True
                        break
                
                if has_partitive:
                    adjectives = [child.text for child in token.children if child.dep_ == 'amod']
                    obj_text = token.text
                    if adjectives:
                        obj_text = ' '.join(adjectives) + ' ' + obj_text
                    
                    results['complements'].append({
                        'text': obj_text,
                        'type': 'Complemento Oggetto Partitivo',
                        'description': 'Complemento oggetto preceduto da articolo partitivo'
                    })
                else:
                    results['complements'].append({
                        'text': token.text,
                        'type': 'Complemento Oggetto',
                        'description': 'Risponde alla domanda "Chi? Che cosa?"'
                    })
        
        elif token.dep_ == 'iobj' or token.dep_ == 'obl:arg':
            results['complements'].append({
                'text': token.text,
                'type': 'Complemento di Termine',
                'description': 'Risponde alla domanda "A chi? A che cosa?"'
            })
        
        elif token.dep_ == 'det:poss' and token.text.lower() == 'loro' and token.head.dep_ == 'obj':
            results['complements'].append({
                'text': token.text,
                'type': 'Complemento di Termine',
                'description': 'Indica la persona su cui termina l\'azione'
            })
        
        elif token.dep_ == 'obl' and token.head.pos_ == 'VERB':
            comp_type = 'Complemento Indiretto'
            
            prep = None
            for child in token.children:
                if child.dep_ == 'case':
                    prep = child.text.lower()
                    break
            
            if prep == 'in':
                comp_type = 'Complemento di Stato in Luogo'
            elif prep == 'a':
                comp_type = 'Complemento di Moto a Luogo'
            elif prep == 'da':
                comp_type = 'Complemento di Moto da Luogo'
            elif prep == 'con':
                comp_type = 'Complemento di Compagnia/Unione'
            elif prep == 'di':
                comp_type = 'Complemento di Specificazione'
            
            results['complements'].append({
                'text': token.text,
                'type': comp_type,
                'description': f'{token.text}'
            })
        
        elif token.dep_ == 'nmod':
            results['complements'].append({
                'text': token.text,
                'type': 'Complemento di Specificazione',
                'description': 'Risponde alla domanda "Di chi? Di che cosa?"'
            })
        
        elif token.dep_ == 'advmod' and token.head.pos_ != 'ADJ':
            results['complements'].append({
                'text': token.text,
                'type': 'Complemento Avverbiale',
                'description': 'Modifica il verbo'
            })
        
        if token.dep_ == 'amod':
            adj_text = token.text
            for child in token.children:
                if child.dep_ == 'advmod':
                    adj_text = child.text + ' ' + adj_text
            
            results['other_elements'].append({
                'text': adj_text,
                'type': 'Attributo',
                'description': f'Aggettivo riferito a "{token.head.text}"'
            })
        
        elif token.pos_ == 'CCONJ' or token.dep_ == 'cc':
            results['other_elements'].append({
                'text': token.text,
                'type': 'Congiunzione',
                'description': 'Collega elementi nella frase'
            })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    sentence = data.get('sentence', '')
    
    if not sentence:
        return jsonify({'error': 'Nessuna frase fornita'}), 400
    
    results = analyze_sentence(sentence)
    return jsonify(results)

