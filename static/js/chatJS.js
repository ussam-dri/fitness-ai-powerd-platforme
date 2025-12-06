const menu = document.querySelector('#menu-btn');
const navbar = document.querySelector('.header .navbar');

menu.addEventListener('click', () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
});

window.onscroll = () => {
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
};
/////////////////////////////////////
// Get references to DOM elements
const popupContainer = document.getElementById('popup-container');
const closePopupButton = document.getElementById('close-popup');

// Show the popup when the page loads
window.onload = () => {
  popupContainer.style.display = 'block';
};

// Hide the popup when the close button is clicked
closePopupButton.addEventListener('click', () => {
  popupContainer.style.display = 'none';
});

// Hide the popup when the user clicks outside of it
popupContainer.addEventListener('click', (event) => {
  if (event.target === popupContainer) {
    popupContainer.style.display = 'none';
  }
});

///////////////////////////////////////////////////////////////////////////
let fimg = false;
let ftxt = false;

function startChat() {
  class ChatBot {
    constructor() {
      this.messages = [];
    }

    onSendButton(chatfoter) {
      const userInput = chatfoter.querySelector('.user_input');
      const text = userInput.value.trim();
      if (text === '') {
        return;
      }

      const userMsg = { name: 'User', message: text };
      this.messages.push(userMsg);

      let url = '';
      let name = '';

      if (fimg) {
        url = 'http://127.0.0.1:5000/predictimg';
        name = 'img';
      } else if (ftxt) {
        url = 'http://127.0.0.1:5000/predictxt';
        name = 'txt';
      }

      fetch(url, {
        method: 'POST',
        body: JSON.stringify({ message: text }),
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((result) => {
          const chatMessage = { name: name, message: result.answer };
          this.messages.push(chatMessage);
          this.updateChatContent(chatPart);
          userInput.value = '';
        })
        .catch((error) => {
          console.error('Error:', error);
          this.updateChatContent(chatPart);
          userInput.value = '';
        });
    }

    updateChatContent(chatPart) {
      let html = '';
      this.messages.forEach((message) => {
        if (message.name === 'User') {
          html += `<div class="messages__item--visitor">${message.message}</div>`;
        } else if (message.name === 'img') {
          html += `<div class="messages__item--operator" style="width: 24%;"><img src="${message.message}" alt="image" width="200" height="200"></div>`;
        } else if (message.name === 'txt') {
          html += `<div class="messages__item--operator">${message.message}</div>`;
        }
      });
      const chatContent = chatPart.querySelector('.msg');
      chatContent.innerHTML = html;
    }
  }

  const chatPart = document.querySelector('.chat_part');
  const chatfoter = document.querySelector('.chat_footer');
  const chatbot = new ChatBot();
  const sendBtn = chatfoter.querySelector('.on_send');

  sendBtn.addEventListener('click', () => {
    chatbot.onSendButton(chatfoter);
  });

  const input = document.querySelector('.user_input');
  input.addEventListener('keyup', function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendBtn.click();
    }
  });
}


////////////////////////////////////////////////////
document.querySelector('.bimage').addEventListener('click', () => {

ftxt=false;
fimg=true;

});
document.querySelector('.btext').addEventListener('click', () => {


ftxt=true;
fimg=false;
});
document.addEventListener('DOMContentLoaded', () => {
startChat();
});