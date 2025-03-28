import React, { useState } from 'react';
import axios from 'axios';
import './VLMInterface.css'; // Create this file for styling

function VLMInterface() {
    const [image, setImage] = useState(null);
    const [textPrompt, setTextPrompt] = useState('');
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleImageChange = (event) => {
        setImage(event.target.files[0]);
    };

    const handleTextPromptChange = (event) => {
        setTextPrompt(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError('');
        setResult('');

        if (!image) {
            setError('Please select an image.');
            setLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('files', image); // Use 'files' to match FastAPI's expected name
        formData.append('text_prompt', textPrompt);

        try {
            const response = await axios.post('http://localhost:8000/process_image/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResult(response.data.result);
        } catch (error) {
            console.error('Error processing image:', error);
            setError('Error processing image. Please check the console for details.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="vlm-interface">
            <h2>VLM Interface</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="image">Image:</label>
                    <input type="file" id="image" onChange={handleImageChange} accept="image/*" />
                </div>
                <div className="form-group">
                    <label htmlFor="textPrompt">Text Prompt:</label>
                    <input
                        type="text"
                        id="textPrompt"
                        value={textPrompt}
                        onChange={handleTextPromptChange}
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Process Image'}
                </button>
            </form>

            {error && <div className="error">{error}</div>}
            {result && (
                <div className="result">
                    <h3>Result:</h3>
                    <p>{result}</p>
                </div>
            )}
        </div>
    );
}

export default VLMInterface;