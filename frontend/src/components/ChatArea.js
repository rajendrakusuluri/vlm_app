import React from 'react';
import InputArea from './InputArea';
import './ChatArea.css';

const ChatArea = ({ messages, inputText, setInputText, onSendMessage, selectedModel, setSelectedModel }) => {
  return (
    <div className="chat-area">
      <div className="message-list">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <span className="message-content">{message.text}</span>
          </div>
        ))}
      </div>
      <InputArea
        inputText={inputText}
        setInputText={setInputText}
        onSendMessage={onSendMessage}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />
    </div>
  );
};

export default ChatArea;