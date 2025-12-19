// InstaQuizAI - Frontend JavaScript
// Handles UI interactions and API communication

// Global state
let currentQuiz = null;
let currentQuestionIndex = 0;
let userAnswers = {};
let currentTopicId = null;

// DOM Elements
const topicSelection = document.getElementById('topic-selection');
const quizScreen = document.getElementById('quiz-screen');
const resultsScreen = document.getElementById('results-screen');
const topicsContainer = document.getElementById('topics-container');
const questionsContainer = document.getElementById('questions-container');
const loading = document.getElementById('loading');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadTopics();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Quiz navigation
    document.getElementById('prev-btn').addEventListener('click', previousQuestion);
    document.getElementById('next-btn').addEventListener('click', nextQuestion);
    document.getElementById('submit-btn').addEventListener('click', submitQuiz);
    
    // Results actions
    document.getElementById('try-again-btn').addEventListener('click', () => {
        showScreen('topic-selection');
        resetQuiz();
    });
    
    document.getElementById('retake-btn').addEventListener('click', () => {
        if (currentTopicId) {
            startQuiz(currentTopicId);
        }
    });
}

// Screen management
function showScreen(screenName) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenName).classList.add('active');
}

function showLoading(show = true) {
    loading.style.display = show ? 'flex' : 'none';
}

// API Calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'API call failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        alert('Error: ' + error.message);
        throw error;
    }
}

// Load topics from backend
async function loadTopics() {
    showLoading(true);
    
    try {
        const result = await apiCall('/get_topics');
        displayTopics(result.topics);
    } catch (error) {
        topicsContainer.innerHTML = '<p style="color: red;">Failed to load topics. Please refresh the page.</p>';
    } finally {
        showLoading(false);
    }
}

// Display topics in grid
function displayTopics(topics) {
    topicsContainer.innerHTML = '';
    
    topics.forEach(topic => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.innerHTML = `
            <h3>${topic.name}</h3>
            <p>${topic.description}</p>
        `;
        topicCard.addEventListener('click', () => startQuiz(topic.id));
        topicsContainer.appendChild(topicCard);
    });
}

// Start a new quiz
async function startQuiz(topicId) {
    currentTopicId = topicId;
    showLoading(true);
    
    try {
        const result = await apiCall('/get_quiz', 'POST', {
            topic_id: topicId,
            num_questions: 5
        });
        
        currentQuiz = result;
        userAnswers = {};
        currentQuestionIndex = 0;
        
        displayQuiz();
        showScreen('quiz-screen');
    } catch (error) {
        // Error already shown in apiCall
    } finally {
        showLoading(false);
    }
}

// Display quiz questions
function displayQuiz() {
    // Update header
    document.getElementById('quiz-topic').textContent = currentQuiz.topic;
    document.getElementById('total-questions').textContent = currentQuiz.questions.length;
    
    // Create question cards
    questionsContainer.innerHTML = '';
    
    currentQuiz.questions.forEach((question, index) => {
        const questionCard = document.createElement('div');
        questionCard.className = 'question-card';
        questionCard.id = `question-${index}`;
        
        const optionsHtml = Object.entries(question.options).map(([key, value]) => `
            <div class="option" data-question-id="${question.id}" data-answer="${key}">
                <span class="option-label">${key}.</span>
                <span class="option-text">${value}</span>
            </div>
        `).join('');
        
        questionCard.innerHTML = `
            <h3>Question ${index + 1}: ${question.question}</h3>
            <div class="options">
                ${optionsHtml}
            </div>
        `;
        
        questionsContainer.appendChild(questionCard);
        
        // Add click handlers to options
        questionCard.querySelectorAll('.option').forEach(option => {
            option.addEventListener('click', () => selectAnswer(option));
        });
    });
    
    // Show first question
    showQuestion(0);
}

// Select an answer
function selectAnswer(optionElement) {
    const questionId = optionElement.dataset.questionId;
    const answer = optionElement.dataset.answer;
    
    // Remove previous selection
    const questionCard = optionElement.closest('.question-card');
    questionCard.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    // Mark new selection
    optionElement.classList.add('selected');
    
    // Store answer
    userAnswers[questionId] = answer;
}

// Show specific question
function showQuestion(index) {
    currentQuestionIndex = index;
    
    // Hide all questions
    document.querySelectorAll('.question-card').forEach(card => {
        card.classList.remove('active');
    });
    
    // Show current question
    document.getElementById(`question-${index}`).classList.add('active');
    
    // Update progress
    document.getElementById('current-question').textContent = index + 1;
    
    // Update navigation buttons
    updateNavigationButtons();
}

// Update navigation button states
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    // Previous button
    prevBtn.disabled = currentQuestionIndex === 0;
    
    // Next and Submit buttons
    const isLastQuestion = currentQuestionIndex === currentQuiz.questions.length - 1;
    
    if (isLastQuestion) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'inline-block';
    } else {
        nextBtn.style.display = 'inline-block';
        submitBtn.style.display = 'none';
    }
}

// Navigation functions
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        showQuestion(currentQuestionIndex - 1);
    }
}

function nextQuestion() {
    if (currentQuestionIndex < currentQuiz.questions.length - 1) {
        showQuestion(currentQuestionIndex + 1);
    }
}

// Submit quiz
async function submitQuiz() {
    // Check if all questions are answered
    const answeredCount = Object.keys(userAnswers).length;
    const totalQuestions = currentQuiz.questions.length;
    
    if (answeredCount < totalQuestions) {
        const confirmSubmit = confirm(
            `You have answered ${answeredCount} out of ${totalQuestions} questions. ` +
            'Unanswered questions will be marked as incorrect. Do you want to submit?'
        );
        
        if (!confirmSubmit) {
            return;
        }
    }
    
    showLoading(true);
    
    try {
        const result = await apiCall('/submit_quiz', 'POST', {
            quiz_id: currentQuiz.quiz_id,
            answers: userAnswers
        });
        
        displayResults(result);
        showScreen('results-screen');
    } catch (error) {
        // Error already shown in apiCall
    } finally {
        showLoading(false);
    }
}

// Display results
function displayResults(results) {
    // Update score display
    document.getElementById('score-percentage').textContent = results.percentage.toFixed(0) + '%';
    document.getElementById('score').textContent = results.score;
    document.getElementById('total').textContent = results.total_questions;
    
    // Performance message
    const performanceText = document.getElementById('performance-text');
    const percentage = results.percentage;
    
    if (percentage >= 80) {
        performanceText.textContent = '🎉 Excellent! You have a great understanding of this topic!';
        performanceText.style.color = '#28a745';
    } else if (percentage >= 60) {
        performanceText.textContent = '👍 Good job! Keep practicing to improve further.';
        performanceText.style.color = '#667eea';
    } else if (percentage >= 40) {
        performanceText.textContent = '📚 Not bad! Review the material and try again.';
        performanceText.style.color = '#ffc107';
    } else {
        performanceText.textContent = '💪 Keep learning! Practice makes perfect.';
        performanceText.style.color = '#dc3545';
    }
    
    // Detailed results
    const resultsList = document.getElementById('results-list');
    resultsList.innerHTML = '';
    
    results.results.forEach((result, index) => {
        const resultItem = document.createElement('div');
        resultItem.className = `result-item ${result.is_correct ? 'correct' : 'incorrect'}`;
        
        const badge = result.is_correct ? '✓ Correct' : '✗ Incorrect';
        const userAnswerText = result.user_answer ? 
            `${result.user_answer}. ${result.options[result.user_answer]}` : 
            'Not answered';
        const correctAnswerText = `${result.correct_answer}. ${result.options[result.correct_answer]}`;
        
        resultItem.innerHTML = `
            <span class="correct-badge">${badge}</span>
            <div class="question-text">Question ${index + 1}: ${result.question}</div>
            <div class="answer-info">
                <strong>Your answer:</strong> ${userAnswerText}
            </div>
            ${!result.is_correct ? `
                <div class="answer-info" style="color: #28a745;">
                    <strong>Correct answer:</strong> ${correctAnswerText}
                </div>
            ` : ''}
        `;
        
        resultsList.appendChild(resultItem);
    });
}

// Reset quiz state
function resetQuiz() {
    currentQuiz = null;
    currentQuestionIndex = 0;
    userAnswers = {};
    currentTopicId = null;
}

// Instagram Integration Placeholder
/*
 * FUTURE FEATURE: Instagram Integration Functions
 * 
 * These functions will be implemented when Instagram integration is added:
 * 
 * 1. authenticateInstagram()
 *    - Handle OAuth flow for Instagram login
 *    - Store access token securely
 *    - Update UI with user's Instagram profile
 * 
 * 2. shareResultsToStory(resultData)
 *    - Generate attractive result card image
 *    - Use Instagram Graph API to post to stories
 *    - Include app branding and score visualization
 * 
 * 3. challengeFriend(quizData)
 *    - Send quiz link via Instagram Direct
 *    - Track friend's completion and score
 *    - Show comparison results
 * 
 * 4. fetchInstagramContent()
 *    - Retrieve educational posts from science accounts
 *    - Display in app for additional learning
 *    - Link to original Instagram posts
 * 
 * Implementation notes:
 * - Requires Instagram App ID and App Secret
 * - Need to handle permissions: instagram_basic, instagram_content_publish
 * - Implement token refresh mechanism
 * - Add privacy controls for user data
 * - Create attractive result card templates
 * - Handle Instagram API rate limits
 */

// Example placeholder function for Instagram sharing
function shareToInstagramStory() {
    // This will be implemented with actual Instagram API integration
    alert('Instagram integration coming soon! You will be able to share your quiz results directly to Instagram Stories.');
}

// Example placeholder function for Instagram challenge
function challengeFriendOnInstagram() {
    // This will be implemented with actual Instagram DM API
    alert('Instagram challenge feature coming soon! You will be able to challenge your friends via Instagram Direct.');
}
