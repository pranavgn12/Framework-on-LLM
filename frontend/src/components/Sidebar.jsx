import { useEffect } from "react";
import { Plus, MessageSquare } from "lucide-react";

import useChat from "../hooks/useChat";

export default function Sidebar({ open }) {

    const {

        chatList,

        selectedChatId,

        loadChats,

        openChat,

        newChat

    } = useChat();

    useEffect(() => {

        loadChats();

    }, []);

    return (

        <div className={`sidebar ${open ? "open" : "closed"}`}>

            <button

                className="new-chat"

                onClick={newChat}

            >

                <Plus size={18} />

                <span>New Chat</span>

            </button>

            <div className="chat-list">

                {

                    chatList.length === 0

                        ?

                        <div className="empty-chat-list">

                            No conversations

                        </div>

                        :

                        chatList.map(chat => (

                            <div

                                key={chat.id}

                                className={`chat-item ${selectedChatId === chat.id
                                        ? "active"
                                        : ""
                                    }`}

                                onClick={() => openChat(chat.id)}

                            >

                                <MessageSquare size={18} />

                                <span>

                                    {chat.title}

                                </span>

                            </div>

                        ))

                }

            </div>

        </div>

    );

}