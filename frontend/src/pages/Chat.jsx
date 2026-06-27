import { useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import ChatWindow from "../components/ChatWindow";
import MessageInput from "../components/MessageInput";

import "../styles/chat.css";

export default function Chat() {

    const [sidebarOpen, setSidebarOpen] = useState(true);

    return (

        <div className="chat-page">

            <Sidebar
                open={sidebarOpen}
            />

            <div className="main-content">

                <Navbar
                    toggleSidebar={() =>
                        setSidebarOpen(!sidebarOpen)
                    }
                />

                <ChatWindow />

                <MessageInput />

            </div>

        </div>

    );

}