# InstaQuizAI

AI-powered MCQ generator for science syllabus issued by Curriculum Development Centre (CDC).

## Overview

InstaQuizAI is an interactive web application that generates Multiple Choice Questions (MCQs) for science topics based on the CDC syllabus. The application features a clean, modern interface for selecting topics, taking quizzes, and viewing detailed results.

## Features

- **Topic Selection**: Choose from Physics, Chemistry, Biology, and Earth Science
- **AI-Generated MCQs**: Placeholder AI function for generating contextual questions (ready for future AI integration)
- **Interactive Quiz Interface**: User-friendly question navigation with instant feedback
- **Score Tracking**: Detailed results with correct/incorrect answers displayed
- **Progress Storage**: SQLite database stores all quizzes and user progress
- **Instagram Integration Ready**: Placeholder buttons and comments for future Instagram features

## Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **SQLite**: Lightweight database for storing topics, quizzes, questions, and progress

### Frontend
- **HTML5**: Semantic markup for structure
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: Interactive functionality without frameworks

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/krispandeya-source/science.git
cd science
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### GET /get_topics
Returns all available science topics from the CDC syllabus.

**Response:**
```json
{
  "success": true,
  "topics": [
    {
      "id": 1,
      "name": "Physics",
      "description": "Mechanics, Thermodynamics, Electricity, and Magnetism"
    }
  ]
}
```

### POST /get_quiz
Generates a new quiz for a selected topic.

**Request:**
```json
{
  "topic_id": 1,
  "num_questions": 5
}
```

**Response:**
```json
{
  "success": true,
  "quiz_id": 1,
  "topic": "Physics",
  "questions": [
    {
      "id": 1,
      "question": "What is the SI unit of force?",
      "options": {
        "A": "Joule",
        "B": "Newton",
        "C": "Watt",
        "D": "Pascal"
      }
    }
  ]
}
```

### POST /submit_quiz
Submits quiz answers and returns score with detailed results.

**Request:**
```json
{
  "quiz_id": 1,
  "answers": {
    "1": "B",
    "2": "A"
  }
}
```

**Response:**
```json
{
  "success": true,
  "score": 2,
  "total_questions": 5,
  "percentage": 40.0,
  "results": [
    {
      "question_id": 1,
      "question": "What is the SI unit of force?",
      "user_answer": "B",
      "correct_answer": "B",
      "is_correct": true
    }
  ]
}
```

## Database Schema

### Tables

**topics**: Stores science topics
- id (PRIMARY KEY)
- name (TEXT)
- description (TEXT)

**quizzes**: Stores quiz instances
- id (PRIMARY KEY)
- topic_id (FOREIGN KEY → topics.id)
- created_at (TIMESTAMP)

**questions**: Stores quiz questions
- id (PRIMARY KEY)
- quiz_id (FOREIGN KEY → quizzes.id)
- question_text (TEXT)
- option_a, option_b, option_c, option_d (TEXT)
- correct_answer (TEXT)

**progress**: Tracks user quiz attempts
- id (PRIMARY KEY)
- quiz_id (FOREIGN KEY → quizzes.id)
- score (INTEGER)
- total_questions (INTEGER)
- completed_at (TIMESTAMP)

## Future Enhancements

### AI Integration
The `generate_mcqs_with_ai()` function is currently a placeholder. Future implementation will include:
- Integration with AI models (OpenAI GPT, Google Gemini, etc.)
- RAG (Retrieval Augmented Generation) with CDC syllabus content
- Dynamic difficulty levels
- Question variety and topic coverage optimization

### Instagram Integration
Placeholder functions and UI elements are ready for:
- **OAuth Authentication**: Login with Instagram account
- **Story Sharing**: Share quiz results as Instagram Stories with attractive templates
- **Friend Challenges**: Send quiz links via Instagram Direct messaging
- **Content Integration**: Display educational content from science Instagram accounts
- **Leaderboards**: Compare scores with friends

Implementation requires:
- Instagram App registration on Meta Developer Portal
- Instagram Basic Display API credentials
- Instagram Graph API for content publishing
- OAuth 2.0 implementation for user authentication

## Project Structure

```
science/
├── app.py                 # Flask backend with API endpoints
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── instaquiz.db          # SQLite database (created on first run)
└── static/               # Frontend files
    ├── index.html        # Main HTML page
    ├── styles.css        # CSS styling
    └── script.js         # JavaScript functionality
```

## Development

### Running in Development Mode
The Flask app runs in debug mode by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar

### Adding New Topics
To add new topics, insert them into the `topics` table:
```python
conn = sqlite3.connect('instaquiz.db')
cursor = conn.cursor()
cursor.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
               ('New Topic', 'Description'))
conn.commit()
conn.close()
```

### Customizing Questions
Modify the `generate_mcqs_with_ai()` function in `app.py` to customize the sample questions or integrate with an AI service.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue on GitHub.
