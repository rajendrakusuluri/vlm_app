import React from 'react';
import './Sidebar.css'; // Create Sidebar.css

const Sidebar = ({ onChatSelect, chatHistory }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">Claude</div>
      <button className="new-chat-button">+ New chat</button>
      <div className="chat-list">
        <div>Chats</div>
        <ul>
          {chatHistory.map((chat) => (
            <li key={chat.id} onClick={() => onChatSelect(chat.id)}>
              {chat.title}
            </li>
          ))}
        </ul>
      </div>
      <div className="profile-section">
        <div className="profile-icon">KR</div> {/* Placeholder */}
        <div className="profile-info">
          <div>KHV RAJENDRA</div>
          <div className="free-plan">Free plan</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;