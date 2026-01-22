// Check if user is selected
if (!storage.hasUser()) {
    window.location.href = 'index.html';
}

// Display user info
const currentUser = storage.getUser();
document.getElementById('userName').textContent = currentUser;
document.getElementById('userAvatar').textContent = currentUser.charAt(0).toUpperCase();

// Load and display skills
async function loadSkills() {
    try {
        const data = await api.get('/skills');
        const container = document.getElementById('skillsContainer');
        const emptyState = document.getElementById('emptyState');

        if (data.skills.length === 0) {
            container.classList.add('hidden');
            emptyState.classList.remove('hidden');
            return;
        }

        container.innerHTML = '';
        container.classList.remove('hidden');
        emptyState.classList.add('hidden');

        data.skills.forEach(skill => {
            const card = createSkillCard(skill);
            container.appendChild(card);
        });
    } catch (error) {
        showAlert('Failed to load skills. Please try again.', 'error');
    }
}

// Create skill card element
function createSkillCard(skill) {
    const card = document.createElement('div');
    card.className = 'card';

    card.innerHTML = `
        <div class="card-header">
            <h3 class="card-title">${skill.skill_name}</h3>
            <span class="card-badge">${skill.count}</span>
        </div>
        <div class="card-content">
            <p><strong>Topic:</strong> ${skill.topic}</p>
            <p style="color: var(--text-muted); font-size: 0.875rem;">
                ${skill.count} template${skill.count !== 1 ? 's' : ''}
            </p>
        </div>
    `;

    return card;
}

// Initialize
loadSkills();
