// Main JavaScript for ResQTrack

// Show toast message
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Fetch cases from backend
async function fetchCases() {
    try {
        const response = await fetch('/cases/all');
        
        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get response text first to check if it's valid JSON
        const responseText = await response.text();
        
        // Try to parse JSON
        let result;
        try {
            result = JSON.parse(responseText);
        } catch (parseError) {
            console.error('Invalid JSON response:', responseText);
            throw new Error('Invalid response from server');
        }
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error fetching cases:', error);
        showToast('Error fetching cases: ' + error.message, 'error');
        return [];
    }
}

// Fetch donations from backend
async function fetchDonations() {
    try {
        const response = await fetch('/donations/all');
        
        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get response text first to check if it's valid JSON
        const responseText = await response.text();
        
        // Try to parse JSON
        let result;
        try {
            result = JSON.parse(responseText);
        } catch (parseError) {
            console.error('Invalid JSON response:', responseText);
            throw new Error('Invalid response from server');
        }
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error fetching donations:', error);
        showToast('Error fetching donations: ' + error.message, 'error');
        return [];
    }
}

// Fetch hospitals from backend
async function fetchHospitals() {
    try {
        const response = await fetch('/hospitals/all');
        
        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get response text first to check if it's valid JSON
        const responseText = await response.text();
        
        // Try to parse JSON
        let result;
        try {
            result = JSON.parse(responseText);
        } catch (parseError) {
            console.error('Invalid JSON response:', responseText);
            throw new Error('Invalid response from server');
        }
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error fetching hospitals:', error);
        showToast('Error fetching hospitals: ' + error.message, 'error');
        return [];
    }
}

// Search hospitals using API
async function searchHospitalsAPI(city) {
    try {
        const response = await fetch(`/hospitals/search?city=${encodeURIComponent(city)}`);
        
        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get response text first to check if it's valid JSON
        const responseText = await response.text();
        
        // Try to parse JSON
        let result;
        try {
            result = JSON.parse(responseText);
        } catch (parseError) {
            console.error('Invalid JSON response:', responseText);
            throw new Error('Invalid response from server');
        }
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error searching hospitals:', error);
        showToast('Error searching hospitals: ' + error.message, 'error');
        return [];
    }
}

// Update case status
async function updateCaseStatus(caseId, status, assignedHospital = '') {
    try {
        const formData = new FormData();
        formData.append('case_id', caseId);
        formData.append('status', status);
        if (assignedHospital) {
            formData.append('assigned_hospital', assignedHospital);
        }
        
        const response = await fetch('/cases/update-status', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message);
            return true;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error updating case status:', error);
        showToast('Error updating case status: ' + error.message, 'error');
        return false;
    }
}

// Render cases table
function renderCasesTable(cases, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (cases.length === 0) {
        container.innerHTML = '<p>No cases found.</p>';
        return;
    }
    
    let tableHTML = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Case ID</th>
                        <th>Reporter</th>
                        <th>Location</th>
                        <th>Animal Type</th>
                        <th>Urgency</th>
                        <th>Status</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    cases.forEach(caseItem => {
        tableHTML += `
            <tr>
                <td>${caseItem.case_id}</td>
                <td>${caseItem.reporter_name}<br>${caseItem.reporter_phone}</td>
                <td>${caseItem.location}</td>
                <td>${caseItem.animal_type}</td>
                <td>${caseItem.urgency}</td>
                <td><span class="status-${caseItem.status.toLowerCase()}">${caseItem.status}</span></td>
                <td>${caseItem.created_at}</td>
                <td>
                    <button class="btn btn-small btn-warning" onclick="openStatusModal('${caseItem.case_id}')">Update</button>
                </td>
            </tr>
        `;
    });
    
    tableHTML += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

// Render donations table
function renderDonationsTable(donations, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (donations.length === 0) {
        container.innerHTML = '<p>No donations found.</p>';
        return;
    }
    
    let tableHTML = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Donor Name</th>
                        <th>Email</th>
                        <th>Amount</th>
                        <th>Category</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    donations.forEach(donation => {
        tableHTML += `
            <tr>
                <td>${donation.donor_name}</td>
                <td>${donation.donor_email}</td>
                <td>₹${donation.amount}</td>
                <td>${donation.category}</td>
                <td>${donation.created_at}</td>
            </tr>
        `;
    });
    
    tableHTML += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

// Render hospitals table
function renderHospitalsTable(hospitals, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (hospitals.length === 0) {
        container.innerHTML = '<p>No hospitals found.</p>';
        return;
    }
    
    let tableHTML = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Phone</th>
                        <th>Location</th>
                        <th>Coordinates</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    hospitals.forEach(hospital => {
        tableHTML += `
            <tr>
                <td>${hospital.name}</td>
                <td>${hospital.address}</td>
                <td>${hospital.phone || 'N/A'}</td>
                <td>${hospital.location}</td>
                <td>${hospital.api_lat}, ${hospital.api_lon}</td>
            </tr>
        `;
    });
    
    tableHTML += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

// Open status update modal
function openStatusModal(caseId) {
    // Set the case ID in the modal
    document.getElementById('updateCaseId').value = caseId;
    
    // Show the modal
    document.getElementById('statusModal').style.display = 'flex';
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
});

// Export functions for use in other scripts
window.showToast = showToast;
window.fetchCases = fetchCases;
window.fetchDonations = fetchDonations;
window.fetchHospitals = fetchHospitals;
window.searchHospitalsAPI = searchHospitalsAPI;
window.updateCaseStatus = updateCaseStatus;
window.renderCasesTable = renderCasesTable;
window.renderDonationsTable = renderDonationsTable;
window.renderHospitalsTable = renderHospitalsTable;
window.openStatusModal = openStatusModal;
window.closeModal = closeModal;