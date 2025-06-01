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
            console.log('Chatbot clicked'); // Debug log
            chatbotWindow.classList.toggle('open');
        });
    }

    if (chatbotCloseBtn && chatbotWindow) {
        chatbotCloseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            chatbotWindow.classList.remove('open');
        });
    }

    // Basic Chatbot send functionality (demo)
    if (chatbotSendBtn && chatInput && chatMessagesContainer) {
        chatbotSendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
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
    const currentPath = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('.sidebar nav ul li a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active'); // Ensure only one is active
        }
    });
    // Special case for ai_diagnosis_results.html to highlight AI Diagnosis
    if (currentPath === 'ai_diagnosis_results.html') {
        const aiDiagLink = document.querySelector('.sidebar nav ul li a[href="ai_diagnosis.html"]');
        if (aiDiagLink) aiDiagLink.classList.add('active');
    }


    // For diagnosis_history.html, populate details on click (demo)
    const historyRows = document.querySelectorAll('.history-list-container tbody tr');
    const detailDate = document.getElementById('detailDate');
    const detailSymptom = document.getElementById('detailSymptom');
    const detailResult = document.getElementById('detailResult');
    const detailRecommendation = document.getElementById('detailRecommendation');

    if (historyRows.length > 0 && detailDate) { // check if on the correct page
        historyRows.forEach(row => {
            row.addEventListener('click', () => {
                // Remove 'active-row' style from previously selected row
                historyRows.forEach(r => r.classList.remove('active-row')); // You'd need to style .active-row
                row.classList.add('active-row');

                const cells = row.getElementsByTagName('td');
                detailDate.textContent = cells[0].textContent;
                detailSymptom.textContent = cells[1].textContent;
                detailResult.textContent = cells[2].textContent;
                // Example recommendation
                detailRecommendation.textContent = "Drink plenty of water, rest. If fever is high or symptoms persist, go to the hospital for examination.";
            });
        });
        // Optionally click the first row by default
        if (historyRows.length > 0) {
           // historyRows[0].click(); // This will trigger the click event listener
        }
    }

});