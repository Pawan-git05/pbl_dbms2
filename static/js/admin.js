// Admin JavaScript for ResQTrack

// Fetch and display statistics
async function loadAdminStats() {
    try {
        const response = await fetch('/admin/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('totalCases').textContent = result.data.total_cases;
            document.getElementById('totalDonations').textContent = result.data.total_donations;
            document.getElementById('totalHospitals').textContent = result.data.total_hospitals;
            document.getElementById('totalAmount').textContent = '$' + result.data.total_amount.toFixed(2);
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        showToast('Error loading statistics: ' + error.message, 'error');
    }
}

// Load all tables
async function loadAllTables() {
    // Load cases
    const cases = await fetchCases();
    renderCasesTable(cases, 'casesTable');
    
    // Load donations
    const donations = await fetchDonations();
    renderDonationsTable(donations, 'donationsTable');
    
    // Load hospitals
    const hospitals = await fetchHospitals();
    renderHospitalsTable(hospitals, 'hospitalsTable');
}

// Search hospitals and display results
async function searchHospitals() {
    const city = document.getElementById('hospitalCity').value.trim();
    
    if (!city) {
        showToast('Please enter a city name', 'error');
        return;
    }
    
    const results = await searchHospitalsAPI(city);
    displayHospitalSearchResults(results);
}

// Display hospital search results
function displayHospitalSearchResults(hospitals) {
    const container = document.getElementById('hospitalSearchResults');
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
                        <th>Latitude</th>
                        <th>Longitude</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    hospitals.forEach(hospital => {
        tableHTML += `
            <tr>
                <td>${hospital.name}</td>
                <td>${hospital.address}</td>
                <td>${hospital.lat}</td>
                <td>${hospital.lon}</td>
                <td>
                    <button class="btn btn-small btn-success" onclick="addHospitalFromAPI('${hospital.name}', '${hospital.address}', '${hospital.lat}', '${hospital.lon}')">Add</button>
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

// Add hospital from API search results
async function addHospitalFromAPI(name, address, lat, lon) {
    try {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('address', address);
        formData.append('location', address.split(',').pop().trim()); // Extract city from address
        formData.append('api_lat', lat);
        formData.append('api_lon', lon);
        
        const response = await fetch('/hospitals/add', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message);
            // Refresh hospitals table
            const hospitals = await fetchHospitals();
            renderHospitalsTable(hospitals, 'hospitalsTable');
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error adding hospital:', error);
        showToast('Error adding hospital: ' + error.message, 'error');
    }
}

// Handle case status update form submission
async function handleStatusUpdate(event) {
    event.preventDefault();
    
    const caseId = document.getElementById('updateCaseId').value;
    const status = document.getElementById('updateStatus').value;
    const assignedHospital = document.getElementById('updateAssignedHospital').value;
    
    const success = await updateCaseStatus(caseId, status, assignedHospital);
    
    if (success) {
        // Close modal
        closeModal('statusModal');
        
        // Refresh cases table
        const cases = await fetchCases();
        renderCasesTable(cases, 'casesTable');
    }
}

// Handle new hospital form submission
async function handleAddHospital(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    try {
        const response = await fetch('/hospitals/add', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message);
            // Reset form
            event.target.reset();
            // Refresh hospitals table
            const hospitals = await fetchHospitals();
            renderHospitalsTable(hospitals, 'hospitalsTable');
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error adding hospital:', error);
        showToast('Error adding hospital: ' + error.message, 'error');
    }
}

// Initialize admin dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Load statistics
    loadAdminStats();
    
    // Load all tables
    loadAllTables();
    
    // Set up form submissions
    const statusForm = document.getElementById('statusUpdateForm');
    if (statusForm) {
        statusForm.addEventListener('submit', handleStatusUpdate);
    }
    
    const hospitalForm = document.getElementById('addHospitalForm');
    if (hospitalForm) {
        hospitalForm.addEventListener('submit', handleAddHospital);
    }
    
    // Set up hospital search
    const searchButton = document.getElementById('searchHospitalBtn');
    if (searchButton) {
        searchButton.addEventListener('click', searchHospitals);
    }
    
    // Set up Enter key for hospital search
    const cityInput = document.getElementById('hospitalCity');
    if (cityInput) {
        cityInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                searchHospitals();
            }
        });
    }
});