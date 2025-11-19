// API Configuration
const API_BASE_URL = 'http://localhost:8000';
let currentUserId = null;
let authCredentials = null;

// Get auth from localStorage
function loadAuth() {
    const stored = localStorage.getItem('healthMonitorAuth');
    if (!stored) {
        window.location.href = '/';
        return false;
    }
    const auth = JSON.parse(stored);
    currentUserId = auth.userId;
    authCredentials = auth.credentials;
    return true;
}

// Make authenticated fetch request
async function authFetch(url, options = {}) {
    if (!authCredentials) {
        window.location.href = '/';
        return;
    }
    
    const headers = {
        'Authorization': 'Basic ' + btoa(authCredentials.username + ':' + authCredentials.password),
        ...options.headers
    };
    
    const response = await fetch(url, { ...options, headers });
    
    if (response.status === 401) {
        localStorage.removeItem('healthMonitorAuth');
        window.location.href = '/';
        return;
    }
    
    return response;
}

// Chart instances
let hrvChart = null;
let heartRateChart = null;
let activityChart = null;

// Utility functions
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
    });
}

function formatDateTime(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit'
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => errorDiv.classList.add('hidden'), 5000);
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function toISOString(date) {
    return date.toISOString();
}

// Initialize date inputs with defaults
function initializeDates() {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    
    document.getElementById('startDate').valueAsDate = startDate;
    document.getElementById('endDate').valueAsDate = endDate;
}

// API calls
async function fetchData(endpoint, userId, startDate, endDate) {
    const start = toISOString(startDate);
    const end = toISOString(endDate);
    const url = `${API_BASE_URL}/api/users/${userId}${endpoint}?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`;
    
    const response = await authFetch(url);
    if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
}

async function fetchOverview(userId, startDate, endDate) {
    const start = toISOString(startDate);
    const end = toISOString(endDate);
    const url = `${API_BASE_URL}/api/users/${userId}/overview?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`;
    
    const response = await authFetch(url);
    if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
}

// Update overview stats
function updateOverviewStats(data) {
    document.getElementById('latestHRV').textContent = 
        data.latest_hrv_ms ? data.latest_hrv_ms.toFixed(1) : '--';
    
    document.getElementById('avgHRV7d').textContent = 
        data.avg_hrv_7d_ms ? data.avg_hrv_7d_ms.toFixed(1) : '--';
    
    document.getElementById('avgHR').textContent = 
        data.latest_hr_avg_bpm ? data.latest_hr_avg_bpm.toFixed(0) : '--';
    
    if (data.hr_min_bpm && data.hr_max_bpm) {
        document.getElementById('hrRange').textContent = 
            `${data.hr_min_bpm.toFixed(0)} - ${data.hr_max_bpm.toFixed(0)}`;
    } else {
        document.getElementById('hrRange').textContent = '--';
    }
}

// Create/update charts
function createHRVChart(data) {
    const ctx = document.getElementById('hrvChart').getContext('2d');
    
    if (hrvChart) {
        hrvChart.destroy();
    }
    
    hrvChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => formatDate(d.day)),
            datasets: [{
                label: 'HRV (ms)',
                data: data.map(d => d.avg_sdnn_ms),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f1f5f9' }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                }
            }
        }
    });
}

function createHeartRateChart(data) {
    const ctx = document.getElementById('heartRateChart').getContext('2d');
    
    if (heartRateChart) {
        heartRateChart.destroy();
    }
    
    heartRateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => formatDate(d.day)),
            datasets: [
                {
                    label: 'Average BPM',
                    data: data.map(d => d.avg_bpm),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Min BPM',
                    data: data.map(d => d.min_bpm),
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Max BPM',
                    data: data.map(d => d.max_bpm),
                    borderColor: '#f59e0b',
                    borderWidth: 1,
                    fill: false,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f1f5f9' }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                }
            }
        }
    });
}

function createActivityChart(data) {
    const ctx = document.getElementById('activityChart').getContext('2d');
    
    if (activityChart) {
        activityChart.destroy();
    }
    
    activityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => formatDate(d.date)),
            datasets: [
                {
                    label: 'Active Energy (kcal)',
                    data: data.map(d => d.active_energy_burned),
                    backgroundColor: 'rgba(124, 58, 237, 0.6)',
                    borderColor: '#7c3aed',
                    borderWidth: 1
                },
                {
                    label: 'Exercise Time (min)',
                    data: data.map(d => d.exercise_time),
                    backgroundColor: 'rgba(79, 70, 229, 0.6)',
                    borderColor: '#4f46e5',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f1f5f9' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                }
            }
        }
    });
}

function getWorkoutIcon(activityType) {
    const icons = {
        'HKWorkoutActivityTypeRunning': '🏃',
        'HKWorkoutActivityTypeWalking': '🚶',
        'HKWorkoutActivityTypeCycling': '🚴',
        'HKWorkoutActivityTypeSwimming': '🏊',
        'HKWorkoutActivityTypeYoga': '🧘',
        'HKWorkoutActivityTypeHiking': '🥾',
        'HKWorkoutActivityTypeStrengthTraining': '💪',
        'HKWorkoutActivityTypeFunctionalStrengthTraining': '🏋️'
    };
    return icons[activityType] || '🏃';
}

function formatWorkoutType(activityType) {
    return activityType
        .replace('HKWorkoutActivityType', '')
        .replace(/([A-Z])/g, ' $1')
        .trim();
}

function renderWorkouts(workouts) {
    const container = document.getElementById('workoutsList');
    
    if (!workouts || workouts.length === 0) {
        container.innerHTML = '<p class="no-data">No workout data available</p>';
        return;
    }
    
    container.innerHTML = workouts.map(workout => `
        <div class="workout-card">
            <div class="workout-icon">${getWorkoutIcon(workout.activity_type)}</div>
            <div class="workout-info">
                <h4>${formatWorkoutType(workout.activity_type)}</h4>
                <div class="workout-details">
                    ${workout.duration ? `
                        <div class="workout-detail">
                            <span>⏱️ Duration:</span>
                            <strong>${workout.duration.toFixed(0)} ${workout.duration_unit || 'min'}</strong>
                        </div>
                    ` : ''}
                    ${workout.total_distance ? `
                        <div class="workout-detail">
                            <span>📏 Distance:</span>
                            <strong>${workout.total_distance.toFixed(2)} ${workout.total_distance_unit || 'km'}</strong>
                        </div>
                    ` : ''}
                    ${workout.total_energy_burned ? `
                        <div class="workout-detail">
                            <span>🔥 Energy:</span>
                            <strong>${workout.total_energy_burned.toFixed(0)} ${workout.total_energy_burned_unit || 'kcal'}</strong>
                        </div>
                    ` : ''}
                </div>
            </div>
            <div class="workout-time">
                ${formatDateTime(workout.start_date)}
            </div>
        </div>
    `).join('');
}

function renderDailySnapshots(snapshots) {
    const container = document.getElementById('snapshotsList');
    
    if (!snapshots || snapshots.length === 0) {
        container.innerHTML = '<p class="no-data">No snapshot data available</p>';
        return;
    }
    
    container.innerHTML = snapshots.map(item => {
        const snapshot = item.snapshot;
        const day = formatDate(item.day);
        
        return `
            <div class="workout-card">
                <div class="workout-icon">📊</div>
                <div class="workout-info">
                    <h4>${day}</h4>
                    <div class="workout-details">
                        ${snapshot.hr ? `
                            <div class="workout-detail">
                                <span>❤️ Heart Rate:</span>
                                <strong>${snapshot.hr.avg_bpm ? snapshot.hr.avg_bpm.toFixed(1) : '--'} ${snapshot.hr.unit || 'bpm'}</strong>
                                <span style="font-size: 0.9em; color: #94a3b8;">
                                    (${snapshot.hr.min_bpm ? snapshot.hr.min_bpm.toFixed(0) : '--'} - ${snapshot.hr.max_bpm ? snapshot.hr.max_bpm.toFixed(0) : '--'})
                                </span>
                            </div>
                        ` : ''}
                        ${snapshot.hrv && snapshot.hrv.avg_sdnn_ms ? `
                            <div class="workout-detail">
                                <span>💓 HRV:</span>
                                <strong>${snapshot.hrv.avg_sdnn_ms.toFixed(1)} ms</strong>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Load all data
async function loadAllData() {
    const userId = currentUserId;
    const startDate = document.getElementById('startDate').valueAsDate;
    const endDate = document.getElementById('endDate').valueAsDate;
    
    if (!startDate || !endDate) {
        showError('Please select both start and end dates');
        return;
    }
    
    if (endDate <= startDate) {
        showError('End date must be after start date');
        return;
    }
    
    showLoading(true);
    
    try {
        // Fetch all data in parallel
        const [overview, hrvData, hrData, activityData, workoutsData, snapshotsData] = await Promise.all([
            fetchOverview(userId, startDate, endDate),
            fetchData('/hrv/daily', userId, startDate, endDate),
            fetchData('/heart-rate/daily', userId, startDate, endDate),
            fetchData('/activity/summary', userId, startDate, endDate),
            fetchData('/workouts', userId, startDate, endDate),
            fetchData('/daily-snapshot', userId, startDate, endDate)
        ]);
        
        // Update UI
        updateOverviewStats(overview);
        
        if (hrvData && hrvData.length > 0) {
            createHRVChart(hrvData);
        }
        
        if (hrData && hrData.length > 0) {
            createHeartRateChart(hrData);
        }
        
        if (activityData && activityData.length > 0) {
            createActivityChart(activityData);
        }
        
        renderWorkouts(workoutsData);
        renderDailySnapshots(snapshotsData);
        
    } catch (error) {
        console.error('Error loading data:', error);
        showError(`Failed to load data: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    if (!loadAuth()) {
        return;
    }
    
    initializeDates();
    
    document.getElementById('loadData').addEventListener('click', loadAllData);
    
    document.getElementById('quickWeek').addEventListener('click', () => {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - 7);
        document.getElementById('startDate').valueAsDate = startDate;
        document.getElementById('endDate').valueAsDate = endDate;
        loadAllData();
    });
    
    document.getElementById('quickMonth').addEventListener('click', () => {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - 30);
        document.getElementById('startDate').valueAsDate = startDate;
        document.getElementById('endDate').valueAsDate = endDate;
        loadAllData();
    });
    
    // Load initial data
    loadAllData();
});
