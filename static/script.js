//const noteDisplay = document.getElementById('noteDisplay');
//const microphoneButton = document.getElementById('microphoneButton');
//const noteInput = document.getElementById('noteInput');
//
//let recognition;
//let isListening = false;
//
//if ('webkitSpeechRecognition' in window) {
//    recognition = new webkitSpeechRecognition();
//    recognition.continuous = true;
//    recognition.interimResults = true;
//    recognition.lang = 'en-US';
//
//    recognition.onresult = (event) => {
//        let transcript = '';
//        for (let i = event.resultIndex; i < event.results.length; i++) {
//            transcript += event.results[i][0].transcript;
//        }
//        noteDisplay.textContent = transcript;
//        noteInput.value = transcript;
//    };
//
//    recognition.onerror = (event) => {
//        console.error('Speech recognition error:', event.error);
//        noteDisplay.textContent = 'Error: ' + event.error;
//    };
//
//    recognition.onend = () => {
//        if (isListening) {
//            recognition.start();
//        }
//    };
//
//    microphoneButton.addEventListener('click', () => {
//        if (isListening) {
//            recognition.stop();
//            isListening = false;
//            microphoneButton.innerHTML = '<i class="fas fa-microphone"></i>';
//        } else {
//            recognition.start();
//            isListening = true;
//            microphoneButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
//            noteDisplay.textContent = 'Listening...';
//        }
//    });
//} else {
//    noteDisplay.textContent = 'Your browser does not support speech recognition. Please use Chrome or another supported browser.';
//    microphoneButton.disabled = true;
//}


const noteDisplay = document.getElementById('noteDisplay');
        const microphoneButton = document.getElementById('microphoneButton');
        const noteInput = document.getElementById('noteInput');

        let recognition;
        let isListening = false;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'hy-AM';  // Հայերենի համար

            recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                noteDisplay.textContent = transcript;
                noteInput.value = transcript;
            };

            recognition.onerror = (event) => {
                console.error('Ձայնի ճանաչման սխալ:', event.error);
                noteDisplay.textContent = 'Սխալ: ' + event.error;
            };

            recognition.onend = () => {
                if (isListening) {
                    recognition.start();
                }
            };

            microphoneButton.addEventListener('click', () => {
                if (isListening) {
                    recognition.stop();
                    isListening = false;
                    microphoneButton.innerHTML = '<i class="fas fa-microphone"></i> Սկսել Ձայնագրել';
                } else {
                    recognition.start();
                    isListening = true;
                    microphoneButton.innerHTML = '<i class="fas fa-microphone-slash"></i> Դադարեցնել Ձայնագրումը';
                    noteDisplay.textContent = 'Լսում եմ...';
                }
            });
        } else {
            noteDisplay.textContent = 'Ձեր բրաուզերը չի աջակցում ձայնի ճանաչումը: Խնդրում ենք օգտագործել Google Chrome:';
            microphoneButton.disabled = true;
        }