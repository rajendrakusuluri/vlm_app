import React from 'react';
import './InputArea.css';

const InputArea = ({ inputText, setInputText, onSendMessage, selectedModel, setSelectedModel }) => {
  return (
    <div className="input-area">
      <textarea
        placeholder="How can I help you today?"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <div className="input-buttons">
        <button>X</button>
        <button>⚙️</button>
      </div>
      <div className="attachment-options">
        <button>Upload a file</button>
        <button>Take a screenshot</button>
        <button>Add from GitHub</button>
      </div>
      <div className="model-selector">
        <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
          <option value="Claude 3.7 Sonnet">Claude 3.7 Sonnet</option>
          <option value="GPT-4">GPT-4 (Example)</option>
        </select>
        <button onClick={onSendMessage}>⬆️</button>
      </div>
    </div>
  );
};

export default InputArea;