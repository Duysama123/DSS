document.addEventListener('DOMContentLoaded', function () {
    // === PHẦN MỚI: LOGIC BẬT/TẮT CHATBOT ===
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotIconContainer = document.getElementById('chatbotIconContainer');
    const chatbotWindow = document.getElementById('chatbotWindow');

    // Hàm để áp dụng cài đặt chatbot
    function applyChatbotSetting() {
        // Lấy giá trị từ localStorage. Nếu chưa có, mặc định là 'true' (bật).
        const isEnabled = localStorage.getItem('chatbotEnabled') !== 'false';
        
        if (chatbotIconContainer) {
            if (isEnabled) {
                chatbotIconContainer.style.display = 'block';
                chatbotIconContainer.classList.remove('hidden');
            } else {
                chatbotIconContainer.style.display = 'none';
                chatbotIconContainer.classList.add('hidden');
                // Đóng cửa sổ chat nếu đang mở
                if (chatbotWindow) {
                    chatbotWindow.classList.remove('open');
                }
            }
        }
        
        // Nếu đang ở trang settings, cập nhật trạng thái của nút gạt
        if (chatbotToggle) {
            chatbotToggle.checked = isEnabled;
        }
    }

    // Luôn gọi hàm này khi tải trang để áp dụng cài đặt đã lưu
    applyChatbotSetting();

    // Thêm sự kiện listener cho nút gạt (nếu có trên trang)
    if (chatbotToggle) {
        chatbotToggle.addEventListener('change', function() {
            // Lưu trạng thái mới vào localStorage
            localStorage.setItem('chatbotEnabled', this.checked);
            // Áp dụng ngay lập tức
            applyChatbotSetting();
        });
    }
    // ==========================================

    // Chatbot toggle
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatbotCloseBtn = document.getElementById('chatbotCloseBtn');
    const chatbotSendBtn = document.getElementById('chatbotSendBtn');
    const chatInput = document.getElementById('chatUserMessage');
    const chatMessagesContainer = document.querySelector('.chatbot-messages');

    // Thêm sự kiện click cho container thay vì chỉ cho icon
    if (chatbotIconContainer && chatbotWindow) {
        chatbotIconContainer.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Chatbot icon clicked'); // Debug log
            chatbotWindow.classList.toggle('open');
        });
    }

    if (chatbotCloseBtn && chatbotWindow) {
        chatbotCloseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Chatbot close button clicked'); // Debug log
            chatbotWindow.classList.remove('open');
        });
    }

    // Basic Chatbot send functionality (demo)
    if (chatbotSendBtn && chatInput && chatMessagesContainer) {
        chatbotSendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent newline
                sendMessage();
            }
        });

        function sendMessage() {
            const messageText = chatInput.value.trim();
            if (messageText === '') return;

            appendMessage(messageText, 'user');
            chatInput.value = '';

            // Simulate bot response
            setTimeout(() => {
                let botResponse = "I'm a demo bot. How can I help you regarding symptoms or medical history?";
                if (messageText.toLowerCase().includes("hello") || messageText.toLowerCase().includes("hi")) {
                    botResponse = "Hello! How can I assist you with the AI Health Diagnosis system today?";
                } else if (messageText.toLowerCase().includes("fever")) {
                    botResponse = "If you have a fever, please describe any other symptoms. Remember, this is not a substitute for professional medical advice.";
                } else if (messageText.toLowerCase().includes("medicine")) {
                     botResponse = "Please list any current medications you are taking when you use the AI Diagnosis feature.";
                }
                appendMessage(botResponse, 'bot');
            }, 1000);
        }

        function appendMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('chat-message', type);
            messageDiv.textContent = text;
            chatMessagesContainer.appendChild(messageDiv);
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight; // Scroll to bottom
        }
    }


    // User dropdown toggle (simple example)
    const userNav = document.querySelector('.user-nav');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (userNav && dropdownMenu) {
        userNav.addEventListener('click', (event) => {
            // Prevent click on link inside dropdown from closing it immediately
            if (event.target.closest('.dropdown-menu a')) {
                return;
            }
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown if clicked outside
        document.addEventListener('click', (event) => {
            if (!userNav.contains(event.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
    }

    // Active navigation link
    // This part is a bit tricky with multiple HTML files without a backend.
    // A simple approach is to set it manually in each HTML file or use JS based on URL.
    const currentPath = window.location.pathname; // Get full path, not just the last part
    const navLinks = document.querySelectorAll('.sidebar nav ul li a');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        // Check for exact match for homepage or inclusion for other pages
        if (currentPath === '/' && (linkPath === '{{ url_for(\'index\') }}' || linkPath === '/' || linkPath === '')) { // Explicitly check for homepage URL variations
             link.classList.add('active');
        } else if (currentPath !== '/' && linkPath !== '/' && linkPath !== '{{ url_for(\'index\') }}' && linkPath !== '') { // Exclude homepage links for other pages
            if (currentPath.includes(linkPath)) { // Use includes for partial match for other pages
                link.classList.add('active');
            } else {
                link.classList.remove('active'); // Ensure only one is active
            }
        } else {
             link.classList.remove('active'); // Remove active class for other cases (like other links on homepage, or homepage links on other pages)
        }

    });

    // Special case for ai_diagnosis_results.html to highlight AI Diagnosis - Keep if still needed, but the above might handle it
    // const pathEnd = currentPath.split("/").pop();
    // if (pathEnd === 'ai-diagnosis-results' || pathEnd === 'diagnose') {
    //     const aiDiagLink = document.querySelector(`.sidebar nav ul li a[href="${window.aiDiagnosisUrl}"]`);
    //     if (aiDiagLink) {
    //         navLinks.forEach(link => link.classList.remove('active')); // Remove others
    //         aiDiagLink.classList.add('active');
    //     }
    // }


    // === History Details Display ===
    // HISTORY_DATA will be populated by reading from a data attribute in the HTML
    const historyRows = document.querySelectorAll('.history-list-container tbody tr.history-row');
    const detailsPlaceholder = document.getElementById('details-placeholder');
    const detailedResultsArea = document.getElementById('detailed-results-area');

    // Get the hidden div containing history data
    const historyDataJsonDiv = document.getElementById('history-data-json');
    let HISTORY_DATA = []; // Initialize as empty array

    if (historyDataJsonDiv && historyDataJsonDiv.dataset.history) {
        try {
            // Parse the JSON string from the data attribute
            HISTORY_DATA = JSON.parse(historyDataJsonDiv.dataset.history);
            console.log("DEBUG JS - HISTORY_DATA parsed from data attribute:", HISTORY_DATA);
        } catch (e) {
            console.error("DEBUG JS - Error parsing history data from data attribute:", e);
            HISTORY_DATA = []; // Reset to empty array if parsing fails
        }
    } else {
         console.log("DEBUG JS - #history-data-json not found or data-history attribute is empty.");
    }
    
    // Now HISTORY_DATA should be available and be an array (empty or with data)
    window.HISTORY_DATA = HISTORY_DATA; // Make it globally accessible if needed elsewhere, though click handler will use the local one.


    // Basic Info Spans
    const detailDateSpan = document.getElementById('detailDate');
    const detailUserInputSpan = document.getElementById('detailUserInput');
    const detailPrimaryDiagnosisSpan = document.getElementById('detailPrimaryDiagnosis');
    const detailConfidenceProbabilitySpan = document.getElementById('detailConfidenceProbability');

    // Detailed Sections Containers (Keep these elements in HTML, but maybe hide/clear them in JS)
    const detailedSuggestionsContainer = document.querySelector('#detailed-suggestions .diagnostic-suggestions-grid');
    const detailedGuidanceContainer = document.getElementById('detailed-guidance');
    const detailedWikipediaContainer = document.getElementById('detailed-wikipedia');

    // Also get the recommendation display element based on your image (assuming an element with ID 'detailRecommendation')
    const detailRecommendationSpan = document.getElementById('detailRecommendation'); // You might need to add this element to diagnosis_history.html

    if (historyRows.length > 0 && detailedResultsArea) {

        // Ensure detailed sections are initially hidden
        if (detailedSuggestionsContainer) detailedSuggestionsContainer.style.display = 'none';
        if (detailedGuidanceContainer) detailedGuidanceContainer.style.display = 'none';
        if (detailedWikipediaContainer) detailedWikipediaContainer.style.display = 'none';

        historyRows.forEach(row => {
            row.addEventListener('click', () => {
                console.log("DEBUG JS - History row clicked. Index:", row.dataset.historyIndex);
                // We are now relying on HISTORY_DATA being correctly injected.
                console.log("DEBUG JS - window.HISTORY_DATA at click:", window.HISTORY_DATA);

                // Remove 'active-row' style from previously selected row
                historyRows.forEach(r => r.classList.remove('active-row'));
                row.classList.add('active-row');

                // Get the history entry based on the data-history-index
                const historyIndex = row.dataset.historyIndex;

                // Check if HISTORY_DATA exists and the index is valid
                if (window.HISTORY_DATA && Array.isArray(window.HISTORY_DATA) && HISTORY_DATA.length > historyIndex && HISTORY_DATA[historyIndex]) {
                     const entry = HISTORY_DATA[historyIndex];
                     console.log("DEBUG JS - Selected history entry:", entry);

                    // Hide placeholder and show detailed area
                    if (detailsPlaceholder) detailsPlaceholder.style.display = 'none';
                    detailedResultsArea.style.display = 'block';

                    // Populate Basic Info
                    if (detailDateSpan) detailDateSpan.textContent = entry.timestamp || 'N/A';
                    // Use Processed Symptoms if available, otherwise User Input
                    if (detailUserInputSpan) detailUserInputSpan.textContent = (entry.processed_symptoms && entry.processed_symptoms.length > 0 ? entry.processed_symptoms.join(', ') : entry.user_input_text) || 'N/A';
                    // detailProcessedSymptomsSpan is available but we combine into User Input for simplicity per recent image, can populate if needed.
                    // if (detailProcessedSymptomsSpan) detailProcessedSymptomsSpan.textContent = (entry.processed_symptoms && entry.processed_symptoms.length > 0 ? entry.processed_symptoms.join(', ') : 'N/A') || 'N/A';

                    if (detailPrimaryDiagnosisSpan) detailPrimaryDiagnosisSpan.textContent = (entry.primary_diagnosis ? entry.primary_diagnosis.replace('_', ' ').split(' (')[0].trim().replace(/\b\w/g, l => l.toUpperCase()) : 'No Diagnosis') || 'No Diagnosis';
                    if (detailConfidenceProbabilitySpan) detailConfidenceProbabilitySpan.textContent = entry.primary_confidence_or_probability || 'N/A';
                    if (detailRecommendationSpan) {
                         detailRecommendationSpan.textContent = (entry.guidance_package && entry.guidance_package.details && entry.guidance_package.details.description) ? entry.guidance_package.details.description : ''; // Set to empty string if no recommendation
                    }

                    // Render Detailed Sections
                    // Ensure containers are visible
                     if (detailedSuggestionsContainer) detailedSuggestionsContainer.style.display = 'grid'; // Assuming grid display for suggestions
                     if (detailedGuidanceContainer) detailedGuidanceContainer.style.display = 'block';
                     if (detailedWikipediaContainer) detailedWikipediaContainer.style.display = 'block';

                    // Call the rendering functions (assuming they are defined later in the script)
                    // Check if the entry and its nested properties exist before calling render functions
                    if (typeof renderSuggestions === 'function') {
                         renderSuggestions(entry.orchestrated_results_with_details || [], detailedSuggestionsContainer);
                    }
                    if (typeof renderGuidance === 'function') {
                         renderGuidance(entry.guidance_package || {}, detailedGuidanceContainer); // Pass the whole guidance_package
                    }
                    if (typeof renderWikipedia === 'function') {
                        renderWikipedia(entry.guidance_package || {}, detailedWikipediaContainer); // Pass the whole guidance_package
                    }

                } else {
                     // Handle case where history entry is not found or HISTORY_DATA is invalid
                     console.error("History entry or HISTORY_DATA invalid/not found for index:", historyIndex, window.HISTORY_DATA);
                     if (detailsPlaceholder) detailsPlaceholder.style.display = 'block';
                     detailedResultsArea.style.display = 'none';
                     // Clear basic fields if data is not found
                     if (detailDateSpan) detailDateSpan.textContent = 'N/A';
                     if (detailUserInputSpan) detailUserInputSpan.textContent = 'N/A';
                     if (detailPrimaryDiagnosisSpan) detailPrimaryDiagnosisSpan.textContent = 'No Diagnosis';
                     if (detailConfidenceProbabilitySpan) detailConfidenceProbabilitySpan.textContent = 'N/A';
                     if (detailRecommendationSpan) detailRecommendationSpan.textContent = ''; // Clear if data is not found

                      // Hide detailed sections if data is not found
                     if (detailedSuggestionsContainer) detailedSuggestionsContainer.style.display = 'none';
                     if (detailedGuidanceContainer) detailedGuidanceContainer.style.display = 'none';
                     if (detailedWikipediaContainer) detailedWikipediaContainer.style.display = 'none';
                }
            });
        });

        // Optionally click the first row by default on page load if history exists
        // Check if HISTORY_DATA has data before clicking
        setTimeout(() => {
             if (window.HISTORY_DATA && Array.isArray(window.HISTORY_DATA) && window.HISTORY_DATA.length > 0) {
                console.log("DEBUG JS - Clicking first history row on load.");
                historyRows[0].click(); // This will trigger the click event listener
             } else {
                 console.log("DEBUG JS - No history data available on load, not clicking first row.");
             }
        }, 50); // Small delay

    } else if (detailsPlaceholder) {
         // If no history rows, ensure placeholder is visible
         detailsPlaceholder.style.display = 'block';
         if (detailedResultsArea) detailedResultsArea.style.display = 'none';
    }


    // === Symptom Search Filtering ===
    const symptomSearchInput = document.getElementById('symptom_search');
    const searchSymptomsBtn = document.getElementById('search_symptoms_btn');
    const symptomItems = document.querySelectorAll('.symptom-grid .symptom-item');

    if (symptomSearchInput && searchSymptomsBtn && symptomItems.length > 0) {
        // Function to perform the filtering
        function filterSymptoms() {
            const searchTerm = symptomSearchInput.value.toLowerCase();

            symptomItems.forEach(item => {
                const symptomLabel = item.querySelector('label').textContent.toLowerCase();
                if (symptomLabel.includes(searchTerm)) {
                    item.style.display = 'flex'; // Show the item
                } else {
                    item.style.display = 'none'; // Hide the item
                }
            });
        }

        // Attach the filter function to the button click event
        searchSymptomsBtn.addEventListener('click', filterSymptoms);

        // Optional: Also trigger filter on Enter key press in the input field
        symptomSearchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent form submission
                filterSymptoms();
            }
        });
    }

    // === History Search Filtering ===
    const historySearchInput = document.querySelector('.search-bar-container input[type="text"]');

    if (historySearchInput && historyRows.length > 0) {
        function filterHistory() {
            const searchTerm = historySearchInput.value.toLowerCase();

            historyRows.forEach(row => {
                // Get text content from relevant cells (e.g., User Input, Processed Symptoms, Primary Diagnosis)
                // Adjust the cell indices based on your table structure if needed.
                const dateText = row.cells[0] ? row.cells[0].textContent.toLowerCase() : '';
                const userInputText = row.cells[1] ? row.cells[1].textContent.toLowerCase() : '';
                const processedSymptomsText = row.cells[2] ? row.cells[2].textContent.toLowerCase() : '';
                const primaryDiagnosisText = row.cells[3] ? row.cells[3].textContent.toLowerCase() : '';

                // Check if any of the relevant text contents include the search term
                if (dateText.includes(searchTerm) || userInputText.includes(searchTerm) || processedSymptomsText.includes(searchTerm) || primaryDiagnosisText.includes(searchTerm)) {
                    row.style.display = 'table-row'; // Show the row
                } else {
                    row.style.display = 'none'; // Hide the row
                }
            });
        }

        // Attach the filter function to the input event (triggers on typing)
        historySearchInput.addEventListener('input', filterHistory);

        // Optional: Trigger filter on page load in case there's a pre-filled search term (e.g., from browser history)
        // filterHistory(); // Uncomment if needed
    }

}); // Closing the DOMContentLoaded listener

// === Rendering Functions for History Details ===

function renderSuggestions(suggestions, container) {
    console.log("DEBUG JS - renderSuggestions called with:", suggestions);
    if (!container) return;
    container.innerHTML = ''; // Clear previous content

    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = '<p>No detailed suggestions available.</p>';
        container.style.display = 'none'; // Hide the container if empty
        return;
    }

    container.style.display = 'grid'; // Ensure container is visible

    let html = '';
    suggestions.forEach(item => {
        // Using optional chaining and nullish coalescing for safety
        const confidence = item.probability_display || 'N/A';
        const diagnosis = item.disease ? item.disease.replace(/_/g, ' ').trim().replace(/\\b\\w/g, l => l.toUpperCase()) : 'Unknown Diagnosis';

        html += `\n            <div class="diagnostic-card">\n                <h4>${diagnosis}</h4>\n                <p><strong>Confidence:</strong> ${confidence}</p>\n            </div>\n        `;
    });
    container.innerHTML = html;
}

function renderGuidance(guidancePackage, container) {
     console.log("DEBUG JS - renderGuidance called with:", guidancePackage);
    if (!container) return;
    container.innerHTML = ''; // Clear previous content

    const details = guidancePackage ? guidancePackage.details : null;

    if (!details || !details.description) {
         container.innerHTML = '<p>No detailed guidance available.</p>';
         container.style.display = 'none'; // Hide the container if empty
        return;
    }
    
    container.style.display = 'block'; // Ensure container is visible

    let html = '<h3>Detailed Guidance</h3>';
    html += `<p>${details.description}</p>`;

    // Add symptoms if available in guidance details
    if (details.symptoms && details.symptoms.length > 0) {
        html += '<p><strong>Associated Symptoms:</strong> ' + details.symptoms.join(', ') + '</p>';
    }
     // Add treatments if available in guidance details
     if (details.treatments && details.treatments.length > 0) {
        html += '<p><strong>Potential Treatments:</strong> ' + details.treatments.join(', ') + '</p>';
    }

    container.innerHTML = html;
}

function renderWikipedia(guidancePackage, container) {
    console.log("DEBUG JS - renderWikipedia called with:", guidancePackage);
    if (!container) return;
    container.innerHTML = ''; // Clear previous content

    const wikipedia = guidancePackage ? guidancePackage.wikipedia : null;

    if (!wikipedia || !wikipedia.summary) {
        container.innerHTML = '<p>No Wikipedia information available.</p>';
        container.style.display = 'none'; // Hide the container if empty
        return;
    }
    
     container.style.display = 'block'; // Ensure container is visible

    let html = '<h3>Further General Information (from Wikipedia)</h3>';
    html += '<p>' + wikipedia.summary + '</p>';

    if (wikipedia.url) {
        html += `<p><a href="${wikipedia.url}" target="_blank">Read more on Wikipedia</a></p>`;
    }

    container.innerHTML = html;
}