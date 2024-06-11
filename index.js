import React, { useState } from 'react';
import { FaComment, FaTimes } from "react-icons/fa";
import axios from 'axios';
import './chatbot.scss'; // Styling

const Chatbot = () => {
    const [inputValue, setInputValue] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [expanded, setExpanded] = useState(false);
};

const handleChange = (e) => {
    setInputValue(e.target.value);
};

const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputValue.trim() === '') return;

    setIsLoading(true);
    try {
        const response = await axios.get(`YOUR_BACKEND_API_URL/${inputValue}`);
        const botReply = response.data.response;
        setMessages([...messages, { text: inputValue, sender: 'user' }, { text: botReply, sender: 'bot' }]);
        setInputValue('');
    } catch (error) {
        console.error('Error fetching chatbot response:', error);
    } finally {
        setIsLoading(false);
    }
};

const toggleChatbot = () => {
    setExpanded(!expanded);
};

return (
    <div className="chatbot-container">
        {!expanded && 
            <div className="chatbot-button" onClick={toggleChatbot}>
                <FaComment className="chatbot-button-icon"/>
            </div>
        }

        {expanded && 
            <div className="chatbot-content">
                <div className="chatbot-button" onClick={toggleChatbot}>
                    <FaTimes className="chatbot-button-icon"/>
                </div>
                
                <div className="chatbot-messages">
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.sender}`}>
                            {message.text}
                        </div>
                    ))}
                </div>
                <form className="chatbot-form" onSubmit={handleSubmit}>
                    <input className="chatbot-form-input" type="text" value={inputValue} onChange={handleChange} placeholder='Ask me about Anything' />
                    <button className="chatbot-form-button rn-button-style--2 btn-solid" type="submit">Ask Chatbot</button>
                </form>
                {isLoading && <div className="loading-indicator">Thinking...</div>}
            </div>
        }
    </div>
);