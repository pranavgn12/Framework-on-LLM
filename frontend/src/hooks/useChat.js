import { useContext } from "react";

import { AppContext } from "../context/AppContext";

import { getChats, createChat } from "../services/chat";
import { getMessages, sendMessage } from "../services/messages";

export default function useChat() {

    const {

        chatList,
        setChatList,

        selectedChatId,
        setSelectedChatId,

        messages,
        setMessages

    } = useContext(AppContext);


    async function loadChats() {

        try {

            const chats = await getChats();

            setChatList(chats);

            if (chats.length > 0 && selectedChatId === null) {

                await openChat(chats[0].id);

            }

        }

        catch (err) {

            console.error(err);

        }

    }


    async function openChat(chatId) {

        try {

            setSelectedChatId(chatId);

            const history = await getMessages(chatId);

            setMessages(history);

        }

        catch (err) {

            console.error(err);

        }

    }


    async function newChat() {

        try {

            const chat = await createChat("New Conversation");

            setChatList(prev => [

                chat,

                ...prev

            ]);

            setSelectedChatId(chat.id);

            setMessages([]);

        }

        catch (err) {

            console.error(err);

        }

    }


    async function send(text) {

        if (!selectedChatId || !text.trim()) return;

        try {

            const response = await sendMessage(

                selectedChatId,

                text

            );

            if (response.conversation_title) {

                setChatList(prev =>

                    prev.map(chat =>

                        chat.id === selectedChatId

                            ? {

                                ...chat,

                                title: response.conversation_title

                            }

                            : chat

                    )

                );

            }

            const history = await getMessages(

                selectedChatId

            );

            setMessages(history);

        }

        catch (err) {

            console.error(err);

        }

    }


    return {

        chatList,

        selectedChatId,

        messages,

        loadChats,

        openChat,

        newChat,

        send

    };

}