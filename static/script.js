const form = document.getElementById('question-form');
        const questionInput = document.getElementById('question-input');
        const resultsContainer = document.getElementById('results-container');
        const answerEl = document.getElementById('answer');
        const sourcesEl = document.getElementById('sources');

        form.addEventListener('submit', async function(event) {
            // Prevent the default form submission which reloads the page
            event.preventDefault();

            const question = questionInput.value;
            if (!question) return;

            // Show the results container and a loading message
            resultsContainer.style.display = 'block';
            answerEl.textContent = 'Thinking...';
            sourcesEl.innerHTML = '';

            try {
                // Send the question to our FastAPI backend
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                // Display the answer
                answerEl.textContent = data.answer;

                // Display the sources
                if (data.sources && data.sources.length > 0) {
                    data.sources.forEach(source => {
                        const sourceDiv = document.createElement('div');
                        sourceDiv.classList.add('source-doc');
                        // Display filename and page number from metadata
                        const metadata = source.metadata;
                        const fileName = metadata.source.split(/[\\/]/).pop(); // Get just the filename
                        const pageNum = metadata.page ? ` (Page ${metadata.page + 1})` : '';
                        
                        sourceDiv.innerHTML = `
                            <p><strong>Source: ${fileName}${pageNum}</strong></p>
                            <p>${source.page_content}</p>
                        `;
                        sourcesEl.appendChild(sourceDiv);
                    });
                }

            } catch (error) {
                console.error('Error fetching answer:', error);
                answerEl.textContent = 'Sorry, an error occurred. Please check the console and try again.';
            }
        });