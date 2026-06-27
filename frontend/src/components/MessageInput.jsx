import { useState } from "react";

import { Paperclip, Mic, SendHorizontal } from "lucide-react";

import useChat from "../hooks/useChat";

export default function MessageInput() {

    const [text, setText] = useState("");

    const { send } = useChat();

    async function handleSend() {

        if (!text.trim()) return;

        await send(text);

        setText("");

    }

    function handleKeyDown(e) {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            handleSend();

        }

    }

    return (

        <div className="message-input">

            <button>

                <Paperclip size={20} />

            </button>

            <input

                type="text"

                placeholder="Message Mental Health AI..."

                value={text}

                onChange={(e) => setText(e.target.value)}

                onKeyDown={handleKeyDown}

            />

            <button>

                <Mic size={20} />

            </button>

            <button onClick={handleSend}>

                <SendHorizontal size={20} />

            </button>

        </div>

    );

}