// This script will run on the skills.html page
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const path = params.get('path');

    const pageTitle = document.getElementById('page-title');
    const careerDropdown = document.getElementById('career-dropdown-container');
    const skillForm = document.getElementById('skill-form');

    // Store the path for the form submission
    localStorage.setItem('careerPath', path);

    // Show the dropdown only if the user chose the 'gap analysis' path
    if (path === 'gap') {
        pageTitle.textContent = 'Analyze Your Career Path';
        careerDropdown.style.display = 'block';
    } else {
        pageTitle.textContent = 'Find a Career Based on Your Skills';
    }

    skillForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const checkedBoxes = document.querySelectorAll('input[name="skill"]:checked');
        const selectedSkills = Array.from(checkedBoxes).map(cb => cb.value);

        const userPath = localStorage.getItem('careerPath');
        let endpoint = '';
        let body = {};

        if (userPath === 'gap') {
            const careerId = document.getElementById('career-select').value;
            endpoint = 'http://127.0.0.1:5000/gap-analysis';
            body = {
                "career_id": careerId,
                "skill_names": selectedSkills
            };
        } else {
            endpoint = 'http://127.0.0.1:5000/recommend';
            body = {
                "skill_names": selectedSkills
            };
        }
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            
            const result = await response.json();

            if (response.ok) {
                // Add the userPath to the result object before saving
                result.userPath = userPath; 
                localStorage.setItem('careerResult', JSON.stringify(result));
                window.location.href = 'results.html';
            } else {
                alert(`Error: ${result.error}`);
            }

        } catch (error) {
            console.error('Failed to fetch:', error);
            alert('Failed to connect to the server. Make sure it is running!');
        }
    });
});