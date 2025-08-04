import React, { useState, useEffect } from 'react';

function Dashboard() {
    const [streams, setStreams] = useState([]);
    const [alerts, setAlerts] = useState([]);

    // Fetch stream status on component load and every few seconds
    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await fetch('http://localhost:8001/streams/status');
                const data = await response.json();
                setStreams(data.streams);
            } catch (error) {
                console.error("Failed to fetch stream status", error);
            }
        };

        fetchStatus();
        const intervalId = setInterval(fetchStatus, 5000); // Poll every 5 seconds
        return () => clearInterval(intervalId); // Cleanup
    }, []);
    
    // ... logic for starting/stopping streams
    
    return (
        <div className="p-4">
            {/* Display StreamCards and Alerts here */}
        </div>
    );
}
