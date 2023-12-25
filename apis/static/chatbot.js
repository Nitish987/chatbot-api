const chatbotActiveBtn = document.getElementById('chatbotActiveBtn');
const chatbotCloseBtn = document.getElementById('chatbotCloseBtn');
const conceptuneChatbot = document.getElementById('conceptuneChatbot');
const message = document.getElementById('message-content');
const sendBtn = document.getElementById('send-message');
const messageHolder = document.getElementById('chatbox-holder');

function buildMessage(type, message) {
    const div = document.createElement('div');
    if (message.charAt(0) == '[' && message.charAt(message.length - 1) == ']') {
        const formDiv = document.createElement('div');
        formDiv.setAttribute('class', 'emform');
        const formConfig = JSON.parse(message);
        const h5 = document.createElement('h5');
        h5.innerHTML = 'Fill this out';
        formDiv.append(h5);
        Array.from(formConfig).forEach(value => {
            const input = document.createElement('input');
            input.setAttribute('id', value.name); 
            input.setAttribute('name', value.name); 
            input.setAttribute('type', value.type); 
            input.setAttribute('placeholder', value.placeholder);
            formDiv.appendChild(input); 
        });
        const submit = document.createElement('button');
        submit.setAttribute('class', 'emform-submit');
        submit.innerHTML = 'Submit';
        submit.addEventListener('click', event => {
            let data = {};
            formDiv.childNodes.forEach(element => {
                if (element instanceof HTMLInputElement) {
                    data[element.getAttribute('name')] = element.value;
                }
            });
            HttpClient.post(`/chatbot/v1/bot-emform/?project_id=${Credentials.projectId}&api_id=${Credentials.apiId}`, {
                "Authorization": Credentials.apiKey,
                "Content-Type": "application/json",
            }, data).then(res => {
                if (res.success) {
                    const chat = buildMessage('bot', res.data.answer);
                    messageHolder.appendChild(chat);
                }
            });
        });
        formDiv.appendChild(submit)
        div.appendChild(formDiv);
    } else {
        const span = document.createElement('span');
        if (type == 'user') {
            div.setAttribute('class', 'chatbox chatbox-user');
        } else {
            div.setAttribute('class', 'chatbox chatbox-bot');
        }
        span.setAttribute('role', type);
        span.innerHTML = message;
        div.appendChild(span);
    }
    return div;
}

chatbotActiveBtn.addEventListener('click', event => {
    chatbotActiveBtn.style.display = 'none';
    conceptuneChatbot.style.display = 'block';
    HttpClient.get(`/chatbot/v1/bot-greetings/?project_id=${Credentials.projectId}&api_id=${Credentials.apiId}`, {
        "Authorization": Credentials.apiKey,
        "Content-Type": "application/json",
    }).then(res => {
        if (res.success) {
            const chat = buildMessage('bot', res.data.answer);
            messageHolder.appendChild(chat);
        }
    });
});

chatbotCloseBtn.addEventListener('click', event => {
    chatbotActiveBtn.style.display = 'flex';
    conceptuneChatbot.style.display = 'none';
});

sendBtn.addEventListener('click', event => {
    if (message.value != '' || message .value != null) {
        const chat = buildMessage('user', message.value);
        messageHolder.appendChild(chat);
        HttpClient.get(`/chatbot/v1/bot/?project_id=${Credentials.projectId}&api_id=${Credentials.apiId}&query=${message.value}`, {
            "Authorization": Credentials.apiKey,
            "Content-Type": "application/json",
        }).then(res => {
            if (res.success) {
                const chat = buildMessage('bot', res.data.answer);
                messageHolder.appendChild(chat);
            }
        });
        message.value = '';
    }
});