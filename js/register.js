const API_BASE_URL = 'http://localhost:8000';

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => errorDiv.classList.add('hidden'), 5000);
}

// Register form
document.getElementById('registerFormElement').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showError('Passwords do not match');
        return;
    }
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }
        
        // Auto-login after registration
        const auth = {
            userId: data.user_id,
            credentials: {
                username: formData.get('username'),
                password: formData.get('password')
            }
        };
        localStorage.setItem('healthMonitorAuth', JSON.stringify(auth));
        
        // Redirect to upload page
        window.location.href = '/upload';
        
    } catch (error) {
        showError(error.message);
    }
});

// Check if already logged in
if (localStorage.getItem('healthMonitorAuth')) {
    window.location.href = '/upload';
}
