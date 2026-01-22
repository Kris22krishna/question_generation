// Check if user is selected
if (!storage.hasUser()) {
    window.location.href = 'index.html';
}

// Display user info
const currentUser = storage.getUser();
document.getElementById('userName').textContent = currentUser;
document.getElementById('userAvatar').textContent = currentUser.charAt(0).toUpperCase();
document.getElementById('createdBy').value = currentUser;

// Initialize CodeMirror editors
let questionEditor, answerEditor;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Question Template Editor
    questionEditor = CodeMirror.fromTextArea(document.getElementById('questionTemplate'), {
        mode: 'python',
        theme: 'material-darker',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        autoCloseBrackets: true,
        matchBrackets: true,
    });

    // Set default template
    questionEditor.setValue(`# Example: Simple addition question
import random

a = random.randint(1, 10)
b = random.randint(1, 10)

question = f"What is {a} + {b}?"`);

    // Initialize Answer Template Editor
    answerEditor = CodeMirror.fromTextArea(document.getElementById('answerTemplate'), {
        mode: 'python',
        theme: 'material-darker',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        autoCloseBrackets: true,
        matchBrackets: true,
    });

    // Set default template
    answerEditor.setValue(`# Example: Calculate the answer
import random

a = random.randint(1, 10)
b = random.randint(1, 10)

answer = a + b`);
});

// Topic Autocomplete
const topicInput = document.getElementById('topic');
const topicSuggestions = document.getElementById('topicSuggestions');

const handleTopicInput = debounce(async (value) => {
    if (value.length < 1) {
        topicSuggestions.classList.add('hidden');
        return;
    }

    try {
        const data = await api.get(`/topics/suggest?q=${encodeURIComponent(value)}`);

        if (data.suggestions.length === 0) {
            topicSuggestions.classList.add('hidden');
            return;
        }

        topicSuggestions.innerHTML = '';
        data.suggestions.forEach(suggestion => {
            const div = document.createElement('div');
            div.className = 'autocomplete-suggestion';
            div.textContent = suggestion;
            div.addEventListener('click', () => {
                topicInput.value = suggestion;
                topicSuggestions.classList.add('hidden');
                updateFormat();
            });
            topicSuggestions.appendChild(div);
        });

        topicSuggestions.classList.remove('hidden');
    } catch (error) {
        console.error('Topic autocomplete error:', error);
    }
}, 300);

topicInput.addEventListener('input', (e) => {
    handleTopicInput(e.target.value);
});

topicInput.addEventListener('blur', () => {
    // Delay to allow click on suggestion
    setTimeout(() => topicSuggestions.classList.add('hidden'), 200);
});

topicInput.addEventListener('change', updateFormat);

// Skill Name Autocomplete
const skillInput = document.getElementById('skillName');
const skillSuggestions = document.getElementById('skillSuggestions');

const handleSkillInput = debounce(async (value) => {
    const topic = topicInput.value;

    if (!topic) {
        showAlert('Please select a topic first', 'warning');
        return;
    }

    try {
        let url = `/skills/suggest?topic=${encodeURIComponent(topic)}`;
        if (value.length >= 1) {
            url += `&q=${encodeURIComponent(value)}`;
        }

        const data = await api.get(url);

        if (data.suggestions.length === 0) {
            skillSuggestions.classList.add('hidden');
            return;
        }

        skillSuggestions.innerHTML = '';
        data.suggestions.forEach(suggestion => {
            const div = document.createElement('div');
            div.className = 'autocomplete-suggestion';
            div.textContent = suggestion;
            div.addEventListener('click', () => {
                skillInput.value = suggestion;
                skillSuggestions.classList.add('hidden');
                updateFormat();
            });
            skillSuggestions.appendChild(div);
        });

        skillSuggestions.classList.remove('hidden');
    } catch (error) {
        console.error('Skill autocomplete error:', error);
    }
}, 300);

skillInput.addEventListener('input', (e) => {
    handleSkillInput(e.target.value);
});

skillInput.addEventListener('focus', (e) => {
    if (e.target.value.length >= 0) {
        handleSkillInput(e.target.value);
    }
});

skillInput.addEventListener('blur', () => {
    setTimeout(() => skillSuggestions.classList.add('hidden'), 200);
});

skillInput.addEventListener('change', updateFormat);

// Auto-populate format field
async function updateFormat() {
    const topic = topicInput.value;
    const skillName = skillInput.value;

    if (!topic || !skillName) {
        document.getElementById('format').value = '';
        return;
    }

    try {
        const data = await api.get(`/templates/next-format?topic=${encodeURIComponent(topic)}&skill_name=${encodeURIComponent(skillName)}`);
        document.getElementById('format').value = data.next_format;
    } catch (error) {
        console.error('Format calculation error:', error);
        showAlert('Failed to calculate format number', 'error');
    }
}

// Preview functionality
document.getElementById('previewBtn').addEventListener('click', async () => {
    const previewBtn = document.getElementById('previewBtn');
    const hideLoading = showLoading(previewBtn);

    try {
        const questionCode = questionEditor.getValue();
        const answerCode = answerEditor.getValue();
        const type = document.getElementById('type').value;

        if (!questionCode || !answerCode || !type) {
            showAlert('Please fill in question template, answer template, and type', 'warning');
            hideLoading();
            return;
        }

        const data = await api.post('/preview', {
            question_template: questionCode,
            answer_template: answerCode,
            type: type
        });

        hideLoading();

        if (data.error) {
            showAlert(`Preview Error: ${data.error}`, 'error');
            document.getElementById('previewQuestionValue').textContent = 'Error';
            document.getElementById('previewAnswerValue').textContent = data.error;
        } else {
            document.getElementById('previewQuestionValue').textContent = JSON.stringify(data.question, null, 2);
            document.getElementById('previewAnswerValue').textContent = JSON.stringify(data.answer, null, 2);
        }

        document.getElementById('previewSection').classList.remove('hidden');
        document.getElementById('previewSection').scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        hideLoading();
        showAlert(`Preview failed: ${error.message}`, 'error');
    }
});

// Close preview
document.getElementById('closePreview').addEventListener('click', () => {
    document.getElementById('previewSection').classList.add('hidden');
});

// Form submission
document.getElementById('templateForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const saveBtn = document.getElementById('saveBtn');
    const hideLoading = showLoading(saveBtn);

    try {
        const formData = {
            grade: parseInt(document.getElementById('grade').value),
            topic: document.getElementById('topic').value,
            skill_name: document.getElementById('skillName').value,
            format: parseInt(document.getElementById('format').value),
            type: document.getElementById('type').value,
            question_template: questionEditor.getValue(),
            answer_template: answerEditor.getValue(),
            created_by: currentUser,
            updated_by: currentUser
        };

        // Validate all fields
        if (!formData.grade || !formData.topic || !formData.skill_name ||
            !formData.format || !formData.type || !formData.question_template ||
            !formData.answer_template) {
            showAlert('Please fill in all required fields', 'warning');
            hideLoading();
            return;
        }

        const response = await api.post('/templates', formData);

        hideLoading();

        if (response.success) {
            showAlert('Template saved successfully!', 'success');

            // Redirect after 2 seconds
            setTimeout(() => {
                window.location.href = 'skills.html';
            }, 2000);
        } else {
            showAlert('Failed to save template', 'error');
        }

    } catch (error) {
        hideLoading();
        showAlert(`Save failed: ${error.message}`, 'error');
    }
});
