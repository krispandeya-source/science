"""
InstaQuizAI - AI-powered MCQ generator for CDC science syllabus
Flask backend with SQLite database
"""

from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='')
DATABASE = 'instaquiz.db'

# Database initialization
def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Topics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Quizzes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
    ''')
    
    # Questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    ''')
    
    # Progress table to track user quiz attempts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            score INTEGER,
            total_questions INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    ''')
    
    # Insert sample topics if empty
    cursor.execute('SELECT COUNT(*) FROM topics')
    if cursor.fetchone()[0] == 0:
        sample_topics = [
            ('Physics', 'Mechanics, Thermodynamics, Electricity, and Magnetism'),
            ('Chemistry', 'Organic Chemistry, Inorganic Chemistry, and Physical Chemistry'),
            ('Biology', 'Cell Biology, Genetics, Evolution, and Ecology'),
            ('Earth Science', 'Geology, Meteorology, and Oceanography')
        ]
        cursor.executemany('INSERT INTO topics (name, description) VALUES (?, ?)', sample_topics)
    
    conn.commit()
    conn.close()

# Placeholder AI MCQ Generation Function
def generate_mcqs_with_ai(topic_name, num_questions=5):
    """
    Placeholder function for AI-powered MCQ generation
    
    TODO: Integrate with AI models (e.g., OpenAI GPT, Google Gemini) to generate
    contextually relevant MCQs based on CDC syllabus content.
    
    Future enhancements:
    - Connect to AI API for dynamic question generation
    - Parse CDC syllabus PDFs to extract relevant content
    - Use RAG (Retrieval Augmented Generation) for accurate questions
    - Implement difficulty levels (easy, medium, hard)
    
    Args:
        topic_name: Name of the science topic
        num_questions: Number of questions to generate
    
    Returns:
        List of dictionaries containing MCQ data
    """
    # Sample questions for demonstration
    sample_questions = {
        'Physics': [
            {
                'question': 'What is the SI unit of force?',
                'options': {'A': 'Joule', 'B': 'Newton', 'C': 'Watt', 'D': 'Pascal'},
                'correct': 'B'
            },
            {
                'question': 'What is the speed of light in vacuum?',
                'options': {'A': '3 × 10⁸ m/s', 'B': '3 × 10⁶ m/s', 'C': '3 × 10⁵ m/s', 'D': '3 × 10⁷ m/s'},
                'correct': 'A'
            },
            {
                'question': 'Which law states that force equals mass times acceleration?',
                'options': {'A': 'First Law', 'B': 'Second Law', 'C': 'Third Law', 'D': 'Law of Gravity'},
                'correct': 'B'
            },
            {
                'question': 'What is the unit of electric current?',
                'options': {'A': 'Volt', 'B': 'Ohm', 'C': 'Ampere', 'D': 'Coulomb'},
                'correct': 'C'
            },
            {
                'question': 'What type of energy does a moving object possess?',
                'options': {'A': 'Potential', 'B': 'Kinetic', 'C': 'Thermal', 'D': 'Chemical'},
                'correct': 'B'
            }
        ],
        'Chemistry': [
            {
                'question': 'What is the atomic number of Carbon?',
                'options': {'A': '4', 'B': '6', 'C': '8', 'D': '12'},
                'correct': 'B'
            },
            {
                'question': 'What is the pH of pure water?',
                'options': {'A': '0', 'B': '7', 'C': '14', 'D': '1'},
                'correct': 'B'
            },
            {
                'question': 'Which element is essential for respiration?',
                'options': {'A': 'Nitrogen', 'B': 'Carbon dioxide', 'C': 'Oxygen', 'D': 'Hydrogen'},
                'correct': 'C'
            },
            {
                'question': 'What is the chemical formula of water?',
                'options': {'A': 'H₂O', 'B': 'CO₂', 'C': 'O₂', 'D': 'H₂O₂'},
                'correct': 'A'
            },
            {
                'question': 'Which gas is most abundant in Earth\'s atmosphere?',
                'options': {'A': 'Oxygen', 'B': 'Carbon dioxide', 'C': 'Nitrogen', 'D': 'Argon'},
                'correct': 'C'
            }
        ],
        'Biology': [
            {
                'question': 'What is the powerhouse of the cell?',
                'options': {'A': 'Nucleus', 'B': 'Mitochondria', 'C': 'Ribosome', 'D': 'Chloroplast'},
                'correct': 'B'
            },
            {
                'question': 'What is the process by which plants make food?',
                'options': {'A': 'Respiration', 'B': 'Photosynthesis', 'C': 'Digestion', 'D': 'Fermentation'},
                'correct': 'B'
            },
            {
                'question': 'What molecule carries genetic information?',
                'options': {'A': 'Protein', 'B': 'Lipid', 'C': 'DNA', 'D': 'Carbohydrate'},
                'correct': 'C'
            },
            {
                'question': 'How many chambers does the human heart have?',
                'options': {'A': '2', 'B': '3', 'C': '4', 'D': '5'},
                'correct': 'C'
            },
            {
                'question': 'What is the basic unit of life?',
                'options': {'A': 'Atom', 'B': 'Molecule', 'C': 'Cell', 'D': 'Organ'},
                'correct': 'C'
            }
        ],
        'Earth Science': [
            {
                'question': 'Which layer of Earth is the thickest?',
                'options': {'A': 'Crust', 'B': 'Mantle', 'C': 'Outer Core', 'D': 'Inner Core'},
                'correct': 'B'
            },
            {
                'question': 'What causes tides on Earth?',
                'options': {'A': 'Wind', 'B': 'Earth\'s rotation', 'C': 'Moon\'s gravity', 'D': 'Sun\'s heat'},
                'correct': 'C'
            },
            {
                'question': 'What is the most common type of rock?',
                'options': {'A': 'Igneous', 'B': 'Sedimentary', 'C': 'Metamorphic', 'D': 'Volcanic'},
                'correct': 'B'
            },
            {
                'question': 'What percentage of Earth is covered by water?',
                'options': {'A': '50%', 'B': '60%', 'C': '71%', 'D': '85%'},
                'correct': 'C'
            },
            {
                'question': 'Which gas protects Earth from UV radiation?',
                'options': {'A': 'Oxygen', 'B': 'Ozone', 'C': 'Nitrogen', 'D': 'Carbon dioxide'},
                'correct': 'B'
            }
        ]
    }
    
    # Return sample questions for the topic
    questions = sample_questions.get(topic_name, sample_questions['Physics'])
    return questions[:num_questions]

# API Endpoints

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/get_topics', methods=['GET'])
def get_topics():
    """
    Get all available science topics from CDC syllabus
    
    Returns:
        JSON array of topics with id, name, and description
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description FROM topics')
        topics = cursor.fetchall()
        conn.close()
        
        topics_list = [
            {'id': t[0], 'name': t[1], 'description': t[2]}
            for t in topics
        ]
        
        return jsonify({
            'success': True,
            'topics': topics_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/get_quiz', methods=['POST'])
def get_quiz():
    """
    Generate a new quiz for a selected topic
    
    Request body:
        topic_id: ID of the selected topic
        num_questions: (optional) Number of questions, default 5
    
    Returns:
        JSON with quiz_id and questions array
    """
    try:
        data = request.get_json()
        topic_id = data.get('topic_id')
        num_questions = data.get('num_questions', 5)
        
        if not topic_id:
            return jsonify({
                'success': False,
                'error': 'topic_id is required'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get topic name
        cursor.execute('SELECT name FROM topics WHERE id = ?', (topic_id,))
        topic = cursor.fetchone()
        
        if not topic:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Topic not found'
            }), 404
        
        topic_name = topic[0]
        
        # Create new quiz
        cursor.execute('INSERT INTO quizzes (topic_id) VALUES (?)', (topic_id,))
        quiz_id = cursor.lastrowid
        
        # Generate MCQs using AI placeholder function
        mcqs = generate_mcqs_with_ai(topic_name, num_questions)
        
        # Store questions in database
        questions_data = []
        for mcq in mcqs:
            cursor.execute('''
                INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                quiz_id,
                mcq['question'],
                mcq['options']['A'],
                mcq['options']['B'],
                mcq['options']['C'],
                mcq['options']['D'],
                mcq['correct']
            ))
            question_id = cursor.lastrowid
            
            questions_data.append({
                'id': question_id,
                'question': mcq['question'],
                'options': {
                    'A': mcq['options']['A'],
                    'B': mcq['options']['B'],
                    'C': mcq['options']['C'],
                    'D': mcq['options']['D']
                }
            })
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'quiz_id': quiz_id,
            'topic': topic_name,
            'questions': questions_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """
    Submit quiz answers and calculate score
    
    Request body:
        quiz_id: ID of the quiz
        answers: Dictionary mapping question_id to selected answer (A/B/C/D)
    
    Returns:
        JSON with score, total questions, and detailed results
    """
    try:
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        answers = data.get('answers', {})
        
        if not quiz_id:
            return jsonify({
                'success': False,
                'error': 'quiz_id is required'
            }), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get all questions for this quiz
        cursor.execute('''
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer
            FROM questions WHERE quiz_id = ?
        ''', (quiz_id,))
        questions = cursor.fetchall()
        
        if not questions:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Quiz not found'
            }), 404
        
        # Calculate score
        score = 0
        total_questions = len(questions)
        results = []
        
        for q in questions:
            question_id = str(q[0])
            correct_answer = q[6]
            user_answer = answers.get(question_id, '')
            
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            results.append({
                'question_id': q[0],
                'question': q[1],
                'options': {
                    'A': q[2],
                    'B': q[3],
                    'C': q[4],
                    'D': q[5]
                },
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })
        
        # Save progress
        cursor.execute('''
            INSERT INTO progress (quiz_id, score, total_questions)
            VALUES (?, ?, ?)
        ''', (quiz_id, score, total_questions))
        
        conn.commit()
        conn.close()
        
        # Calculate percentage
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        return jsonify({
            'success': True,
            'score': score,
            'total_questions': total_questions,
            'percentage': round(percentage, 2),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Instagram Integration Placeholder
"""
FUTURE FEATURE: Instagram Integration

Planned features for Instagram integration:
1. Share quiz results as Instagram Stories
   - Generate attractive result cards with score/percentage
   - Use Instagram Graph API to post stories
   - Include branding and CDC syllabus reference

2. Challenge friends via Instagram DM
   - Send quiz links through Instagram Direct messaging
   - Track friend scores and create leaderboards
   - Use Instagram Messaging API

3. Instagram authentication
   - OAuth 2.0 flow for Instagram login
   - Link user's quiz progress to Instagram account
   - Display Instagram profile in app

4. Instagram content integration
   - Fetch educational content from science Instagram accounts
   - Integrate visual learning materials
   - Cross-promote on Instagram platform

Implementation TODO:
- Register app on Meta/Facebook Developer portal
- Obtain Instagram Basic Display API credentials
- Implement OAuth flow for user authentication
- Create story templates for result sharing
- Add Instagram sharing buttons to UI
- Implement Instagram Graph API calls for posting
- Add privacy settings for Instagram integration
"""

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
