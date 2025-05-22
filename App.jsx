import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

import { IoSend, IoCodeDownload } from 'react-icons/io5';
import { BiCodeAlt } from "react-icons/bi";
import { SiPython, SiAdobeillustrator } from "react-icons/si";

const App = () => {
  const [message, setMessage] = useState("");
  const [isResponseScreen, setisResponseScreen] = useState(false);
  const [messages, setMessages] = useState([]);

  const hitRequest = () => {
    if (message) {
      generateResponse(message);
    } else {
      alert("You must write something...!");
    }
  };

  const generateResponse = async (msg) => {
    try {
      const res = await axios.post('http://localhost:5000/chat', { message: msg });


      const newMessages = [
        ...messages,
        { type: "userMsg", text: msg },
        { type: "responseMsg", text: res.data.response || "⚠️ No response from backend." },
      ];

      setMessages(newMessages);
      setisResponseScreen(true);
      setMessage("");
    } catch (error) {
      const newMessages = [
        ...messages,
        { type: "userMsg", text: msg },
        { type: "responseMsg", text: `❌ Error: ${error.message}` },
      ];

      setMessages(newMessages);
      setisResponseScreen(true);
      setMessage("");
    }
  };

  const newChat = () => {
    setisResponseScreen(false);
    setMessages([]);
  };

  return (
    <div className="container w-screen min-h-screen overflow-x-hidden bg-[#0080FF] text-black">
      {isResponseScreen ? (
        <div className='h-[80vh]'>
          <div className="header pt-[25px] flex items-center justify-between w-[100vw] px-[300px]">
            <h2 className='text-4xl'>Chat Interface</h2>
            <button className='bg-[#181818] p-[10px] rounded-[30px] cursor-pointer text-[14px] px-[20px]' onClick={newChat}>New Chat</button>
          </div>
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={msg.type}>{msg.text}</div>
            ))}
          </div>
        </div>
      ) : (
        <div className="middle h-[80vh] flex items-center flex-col justify-center">
          <h1 className='text-4xl'>Chat Interface</h1>
          <div className="boxes mt-[30px] flex items-center gap-2 flex-wrap">
            <Card text={<>Finding new coding?<br />How we can learn it.</>} icon={<IoCodeDownload />} />
            <Card text={<>Which language is easy to learn<br />for coding and programming</>} icon={<BiCodeAlt />} />
            <Card text={<>In which year Python<br />was invented?</>} icon={<SiPython />} />
            <Card text={<>How can we use<br />AI to adapt?</>} icon={<SiAdobeillustrator />} />
          </div>
        </div>
      )}

      <div className="bottom w-full flex flex-col items-center">
        <div className="inputBox w-[60%] text-[15px] py-[7px] flex items-center bg-[#181818] rounded-[30px]">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            type="text"
            className='p-[10px] pl-[15px] bg-transparent flex-1 outline-none border-none'
            placeholder='Write your message here...'
          />
          {message !== "" && (
            <i className='text-green-500 text-[20px] mr-5 cursor-pointer' onClick={hitRequest}><IoSend /></i>
          )}
        </div>
        <p className='text-[gray] text-[14px] my-4'>Chat interface is powered by AI</p>
      </div>
    </div>
  );
};

const Card = ({ text, icon }) => (
  <div className="card rounded-lg cursor-pointer transition-all hover:bg-[#201f1f] px-[20px] relative min-h-[20vh] bg-[#181818] p-[10px]">
    <p className='text-[18px] whitespace-pre-line'>{text}</p>
    <i className='absolute right-3 bottom-3 text-[18px]'>{icon}</i>
  </div>
);

export default App;
