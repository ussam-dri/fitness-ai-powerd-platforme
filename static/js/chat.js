//////////////////////: THIS IS USLESS :://///////////////////////////////////////////
class Chatbox {

    constructor() {


        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }




///////////////////////////////////////////////////
    onSendButton(chatbox) {
    console.log('cik');
     var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
 // for text

 //////////////////////////////////////////////////////////////////////////////////////////////////////



    //  for image
    //////////////////////////////////////////////////////////////////////////////////////////////////////
    fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: 'txt', message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }



    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "img")
            {

               html += '<div class="messages__item messages__item--visitor">' +
                    '<img src="' + item.message + '" alt="image" width="200" height="200">' +
                    '</div>';
            }
            else if (item.name === "txt")
            {
               html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'

            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }


          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();

