// frontend/src/App.js
import React, { useState, useEffect } from 'react';
// The following CSS files were removed as they do not exist in the project structure.
// The styling is handled by Tailwind CSS, which is assumed to be configured separately.
import './App.css';
import './index.css';

// The main application component for the VMS dashboard.
const App = () => {
  // State to hold the message from the backend.
  const [backendMessage, setBackendMessage] = useState('Connecting to backend...');
  const [loading, setLoading] = useState(true);

  // useEffect hook to fetch data from the backend when the component mounts.
  useEffect(() => {
    const fetchMessage = async () => {
      try {
        // We use a relative path '/' because the proxy is configured in package.json
        // to forward requests to the FastAPI backend.
        const response = await fetch('http://localhost:8001/');
        
        // Handle non-200 responses
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setBackendMessage(data.message);
      } catch (error) {
        console.error("Failed to fetch from backend", error);
        console.log(error);
        setBackendMessage('Failed to connect to backend.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchMessage();
  }, []); // The empty dependency array ensures this runs only once on component mount.

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="p-6 bg-white rounded-lg shadow-md max-w-sm w-full text-center">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Frontend Status</h1>
        {/* Display a loading state or the message from the backend. */}
        {loading ? (
          <p className="text-lg text-gray-500 animate-pulse">Loading...</p>
        ) : (
          <p className="mt-4 text-lg text-gray-600">
            Backend Message: <span className="font-semibold text-blue-600">{backendMessage}</span>
          </p>
        )}
      </div>
    </div>
  );
};

export default App;
