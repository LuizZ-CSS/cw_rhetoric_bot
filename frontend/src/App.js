import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [alignment, setAlignment] = useState(2);
    const [sceneStyle, setSceneStyle] = useState(0);
    const [prevAlignment, setPrevAlignment] = useState(2);
    const [prevSceneStyle, setPrevSceneStyle] = useState(0);

    const alignmentLabels = ["Strongly pro-USA", "Slightly pro-USA", "Neutral", "Slightly pro-USSR", "Strongly pro-USSR"];
    const sceneStyleLabels = ["Interview", "Diplomatic Dinner", "Classroom", "Street Conversation", "Private Letter"];

    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => {
        if (alignment !== prevAlignment) {
            setMessages(prev => [...prev, {
                sender: "System",
                text: `Political alignment shifted to ${alignmentLabels[alignment]}`,
                isBackground: true
            }]);
            setPrevAlignment(alignment);
        }
    }, [alignment]);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => {
        if (sceneStyle !== prevSceneStyle) {
            setMessages(prev => [...prev, {
                sender: "System",
                text: `Scene style changed to ${sceneStyleLabels[sceneStyle]}`,
                isBackground: true
            }]);
            setPrevSceneStyle(sceneStyle);
        }
    }, [sceneStyle]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: "User", text: input };
        setMessages([...messages, userMessage]);
        setIsLoading(true);

        try {
            const res = await axios.get(`/ask?q=${encodeURIComponent(input)}&alignment=${alignment}&scene=${sceneStyle}`);
            const botMessage = { sender: "Rhetorica", text: res.data.response };
            setMessages([...messages, userMessage, botMessage]);
        } catch (error) {
            console.error("Error:", error);
            setMessages([...messages, userMessage, { sender: "Rhetorica", text: "I apologize, but I encountered an error. Please try again." }]);
        } finally {
            setIsLoading(false);
            setInput("");
        }
    };

    return (
        <div style={{
            maxWidth: "1600px",
            margin: "0 auto",
            padding: "20px",
            fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif"
        }}>
            <h1 style={{
                textAlign: "center",
                color: "#2c3e50",
                marginBottom: "30px",
                fontSize: "2.5rem"
            }}>Rhetorica Chatbot</h1>

            <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "20px",
                marginBottom: "20px",
                padding: "20px",
                backgroundColor: "#f8f9fa",
                borderRadius: "12px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
            }}>
                <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                    <div>
                        <label style={{ fontWeight: "600", display: "block", marginBottom: "8px" }}>Political Alignment</label>
                        {alignmentLabels.map((label, idx) => (
                            <label key={idx} style={{ display: "inline-block", marginRight: "20px" }}>
                                <input
                                    type="radio"
                                    name="alignment"
                                    value={idx}
                                    checked={alignment === idx}
                                    onChange={() => setAlignment(idx)}
                                    style={{ marginRight: "6px" }}
                                />
                                {label}
                            </label>
                        ))}
                    </div>

                    <div>
                        <label style={{ fontWeight: "600", display: "block", marginBottom: "8px" }}>Scene Style</label>
                        {sceneStyleLabels.map((label, idx) => (
                            <label key={idx} style={{ display: "inline-block", marginRight: "20px" }}>
                                <input
                                    type="radio"
                                    name="scene"
                                    value={idx}
                                    checked={sceneStyle === idx}
                                    onChange={() => setSceneStyle(idx)}
                                    style={{ marginRight: "6px" }}
                                />
                                {label}
                            </label>
                        ))}
                    </div>
                </div>
            </div>

            <div style={{
                height: "60vh",
                overflowY: "auto",
                border: "1px solid #e0e0e0",
                borderRadius: "12px",
                padding: "20px",
                backgroundColor: "#f8f9fa",
                marginBottom: "20px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                position: "relative"
            }}>
                {messages.map((msg, index) => (
                    msg.isBackground ? (
                        <div key={index} style={{
                            position: "absolute",
                            top: "0",
                            left: "0",
                            right: "0",
                            padding: "8px 16px",
                            backgroundColor: "rgba(233, 236, 239, 0.9)",
                            borderBottom: "1px solid #dee2e6",
                            fontSize: "0.9rem",
                            color: "#6c757d",
                            fontStyle: "italic",
                            zIndex: 1
                        }}>
                            {msg.text}
                        </div>
                    ) : (
                        <div key={index} style={{
                            display: "flex",
                            justifyContent: msg.sender === "User" ? "flex-end" : "flex-start",
                            marginBottom: "15px",
                            marginTop: msg.isBackground ? "40px" : "0"
                        }}>
                            <div style={{
                                maxWidth: "70%",
                                padding: "12px 16px",
                                borderRadius: "16px",
                                backgroundColor: msg.sender === "User" ? "#007bff" : "#ffffff",
                                color: msg.sender === "User" ? "#ffffff" : "#2c3e50",
                                boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
                                fontSize: "1rem",
                                lineHeight: "1.4"
                            }}>
                                <div style={{ fontWeight: "600", marginBottom: "4px" }}>
                                    {msg.sender}
                                </div>
                                {msg.text}
                            </div>
                        </div>
                    )
                ))}
                {isLoading && (
                    <div style={{
                        display: "flex",
                        justifyContent: "flex-start",
                        marginBottom: "15px"
                    }}>
                        <div style={{
                            padding: "12px 16px",
                            borderRadius: "16px",
                            backgroundColor: "#ffffff",
                            boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
                            display: "flex",
                            alignItems: "center",
                            gap: "8px"
                        }}>
                            <div style={{
                                width: "20px",
                                height: "20px",
                                border: "3px solid #f3f3f3",
                                borderTop: "3px solid #007bff",
                                borderRadius: "50%",
                                animation: "spin 1s linear infinite"
                            }} />
                            <span style={{ color: "#6c757d" }}>Thinking...</span>
                        </div>
                    </div>
                )}
            </div>

            <div style={{
                display: "flex",
                gap: "10px",
                padding: "0 10px"
            }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && !isLoading && sendMessage()}
                    placeholder="Type your message..."
                    style={{
                        flex: 1,
                        padding: "12px 16px",
                        border: "1px solid #e0e0e0",
                        borderRadius: "8px",
                        fontSize: "1rem",
                        outline: "none",
                        transition: "border-color 0.2s",
                        boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
                    }}
                    disabled={isLoading}
                />
                <button 
                    onClick={sendMessage} 
                    disabled={isLoading}
                    style={{
                        padding: "12px 24px",
                        backgroundColor: "#007bff",
                        color: "white",
                        border: "none",
                        borderRadius: "8px",
                        fontSize: "1rem",
                        cursor: "pointer",
                        transition: "background-color 0.2s",
                        boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
                    }}
                    onMouseOver={e => e.target.style.backgroundColor = "#0056b3"}
                    onMouseOut={e => e.target.style.backgroundColor = "#007bff"}
                >
                    Send
                </button>
            </div>

            <style>
                {`
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}
            </style>
        </div>
    );
}

export default App;
