import { useState } from "react";
import axios from "axios";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await axios.post("http://localhost:8000/chat", { query: input });
      setMessages([...newMessages, { text: response.data.answer, sender: "bot" }]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <div>
        {messages.map((msg, index) => (
          <p key={index} style={{ color: msg.sender === "user" ? "blue" : "green" }}>
            {msg.text}
          </p>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask me anything..." />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbot;
