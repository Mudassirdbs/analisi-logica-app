const sentenceInput = document.getElementById('sentenceInput');
const analyzeButton = document.getElementById('analyzeButton');
const micButton = document.getElementById('micButton');
const resultsSection = document.getElementById('resultsSection');
const subjectResults = document.getElementById('subjectResults');
const predicateResults = document.getElementById('predicateResults');
const complementsResults = document.getElementById('complementsResults');
const otherElementsResults = document.getElementById('otherElementsResults');
const fullAnalysis = document.getElementById('fullAnalysis');

let recognition;
let isRecording = false;

function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'it-IT';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            isRecording = true;
            micButton.classList.add('recording');
            micButton.textContent = '🔴 Registrando...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            sentenceInput.value = transcript;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            showError('Errore nel riconoscimento vocale. Assicurati di aver concesso i permessi per il microfono.');
        };

        recognition.onend = () => {
            isRecording = false;
            micButton.classList.remove('recording');
            micButton.textContent = '🎤 Parla';
        };
    } else {
        micButton.disabled = true;
        micButton.textContent = '❌ Non supportato';
        micButton.title = 'Il riconoscimento vocale non è supportato dal tuo browser';
    }
}

micButton.addEventListener('click', () => {
    if (!recognition) return;
    
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
    }
});

analyzeButton.addEventListener('click', analyzeSentence);

sentenceInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeSentence();
    }
});

document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        sentenceInput.value = btn.dataset.example;
        analyzeSentence();
    });
});

async function analyzeSentence() {
    const sentence = sentenceInput.value.trim();
    
    if (!sentence) {
        showError('Per favore, inserisci una frase da analizzare.');
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = '⏳ Analizzando...';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sentence }),
        });

        if (!response.ok) {
            throw new Error('Errore nell\'analisi');
        }

        const data = await response.json();
        displayResults(data);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        console.error('Error:', error);
        showError('Si è verificato un errore durante l\'analisi. Riprova.');
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = '✨ Analizza';
    }
}

function displayResults(data) {
    subjectResults.innerHTML = '';
    predicateResults.innerHTML = '';
    complementsResults.innerHTML = '';
    otherElementsResults.innerHTML = '';
    fullAnalysis.innerHTML = '';

    if (data.subject && data.subject.length > 0) {
        data.subject.forEach(item => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `<strong>${item.text}</strong> - ${item.description}`;
            subjectResults.appendChild(div);
        });
    } else {
        subjectResults.innerHTML = '<p style="color: var(--text-secondary);">Nessun soggetto identificato.</p>';
    }

    if (data.predicate && data.predicate.length > 0) {
        data.predicate.forEach(item => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `<strong>${item.text}</strong> - ${item.description}`;
            predicateResults.appendChild(div);
        });
    } else {
        predicateResults.innerHTML = '<p style="color: var(--text-secondary);">Nessun predicato identificato.</p>';
    }

    if (data.complements && data.complements.length > 0) {
        data.complements.forEach(item => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `<strong>${item.text}</strong> - ${item.type}<br><small>${item.description}</small>`;
            complementsResults.appendChild(div);
        });
    } else {
        complementsResults.innerHTML = '<p style="color: var(--text-secondary);">Nessun complemento identificato.</p>';
    }

    if (data.other_elements && data.other_elements.length > 0) {
        data.other_elements.forEach(item => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `<strong>${item.text}</strong> - ${item.type}<br><small>${item.description}</small>`;
            otherElementsResults.appendChild(div);
        });
    } else {
        otherElementsResults.innerHTML = '<p style="color: var(--text-secondary);">Nessun altro elemento identificato.</p>';
    }

    if (data.tokens && data.tokens.length > 0) {
        const table = document.createElement('table');
        table.className = 'analysis-table';
        
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Parola</th>
                <th>Lemma</th>
                <th>Categoria</th>
                <th>Funzione</th>
                <th>Dipendente da</th>
            </tr>
        `;
        table.appendChild(thead);
        
        const tbody = document.createElement('tbody');
        data.tokens.forEach(token => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${token.text}</strong></td>
                <td>${token.lemma}</td>
                <td>${token.pos}</td>
                <td>${token.dep}</td>
                <td>${token.head}</td>
            `;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        fullAnalysis.appendChild(table);
    }
}

function showError(message) {
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.container');
    const inputSection = document.querySelector('.input-section');
    container.insertBefore(errorDiv, inputSection.nextSibling);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

initSpeechRecognition();
