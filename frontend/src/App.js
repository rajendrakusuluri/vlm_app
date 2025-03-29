import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import Footer from './components/Footer';
import './App.css'; // You'll need to create this file

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [selectedModel, setSelectedModel] = useState('Claude 3.7 Sonnet');

  useEffect(() => {
    // Simulate loading chat history from an API (replace with actual API call)
    const fakeChatHistory = [
      { id: 1, title: 'Chat 1' },
      { id: 2, title: 'Chat 2' },
    ];
    setChatHistory(fakeChatHistory);
    //For testing purposes only, remove after creating real chat history with API
    setMessages([{sender:"vlm", text: "Hi Rajendra, how are you?"}]);
  }, []);

  const handleSendMessage = async () => {
    if (inputText.trim() === '') return;

    // Add user message to the state
    setMessages([...messages, { sender: 'user', text: inputText }]);

    // Simulate API call (replace with actual API call)
    setTimeout(() => {
      const fakeResponse = `VLM response to: ${inputText}`;
      setMessages((prevMessages) => [...prevMessages, { sender: 'vlm', text: fakeResponse }]);
      setInputText(''); // Clear the input after sending
    }, 500);
  };

  const handleChatSelect = (chatId) => {
    setCurrentChatId(chatId);
    // Simulate loading chat messages from an API based on chatId
    // (replace with actual API call)
    setMessages([{ sender: 'vlm', text: `Loaded chat history for chat ID: ${chatId}` }]);
  };

  return (
    <div className="app-container">
      <Sidebar onChatSelect={handleChatSelect} chatHistory={chatHistory} />
      <div className="main-content">
        <ChatArea
          messages={messages}
          inputText={inputText}
          setInputText={setInputText}
          onSendMessage={handleSendMessage}
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
        />
        <Footer />
      </div>
    </div>
  );
}

export default App;