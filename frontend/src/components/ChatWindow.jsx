import useChat from "../hooks/useChat";

export default function ChatWindow() {

    const {

        chatList,

        selectedChatId,

        messages

    } = useChat();


    const selectedChat = chatList.find(

        chat => chat.id === selectedChatId

    );


    return (

        <div className="chat-window">

            <div className="chat-header">

                <h2>

                    {

                        selectedChat

                            ? selectedChat.title

                            : "Mental Health AI"

                    }

                </h2>

            </div>


            <div className="messages">

                {

                    messages.length === 0

                        ?

                        <div className="empty-chat">

                            <h2>👋 Welcome</h2>

                            <p>

                                Start a conversation.

                            </p>

                        </div>

                        :

                        messages.map(message => (

                            <div

                                key={message.id}

                                className={`message-row ${message.role}`}

                            >

                                <div className="bubble">

                                    {message.content}

                                </div>

                            </div>

                        ))

                }

            </div>

        </div>

    );

}