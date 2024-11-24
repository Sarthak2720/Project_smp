import React, { useState, useEffect } from 'react';
import { CheckCircle2 } from 'lucide-react';

const Stage2 = () => {
  const [platform, setPlatform] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const storedPlatform = sessionStorage.getItem('platform');
    const storedUsername = sessionStorage.getItem('username');
    const storedPassword = sessionStorage.getItem('password');

    if (storedPlatform && storedUsername && storedPassword) {
      setPlatform(storedPlatform);
      setUsername(storedUsername);
      setPassword(storedPassword);
    } else {
      setMessage('Error: Missing credentials. Please return to Stage1.');
    }
  }, []);

  const handleButtonClick = async (option) => {
    setMessage('');
    setIsLoading(true);

    try {
      if (!platform || !username || !password) {
        setMessage('Error: Missing credentials.');
        setIsLoading(false);
        return;
      }

      const response = await fetch('http://localhost:5000/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ platform, username, password, option }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${platform}_${option.replace(' ', '_')}.pdf`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        setMessage('File downloaded successfully.');
      } else {
        const data = await response.json();
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      setMessage('Error occurred during parsing. Please try again.');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleParseAll = async () => {
    await handleButtonClick('Parse All');
  };

  return (
    <div className="loginContainer h-[70vh] flex flex-col gap-6 rounded-md w-[30vw] border-2 border-black bg-white">
      <div className="flex justify-evenly p-6">
        <CheckCircle2 className="bg-green-500 rounded-full" />
        <CheckCircle2 className="bg-green-500 rounded-full" />
        <p className="rounded-full border border-black px-2 py-1">3</p>
      </div>

      <h1 className="text-3xl text-center font-medium">Parsing Options</h1>

      {platform && username ? (
        <p className="text-center text-lg">
          Logged into <strong>{platform.toUpperCase()}</strong> as{' '}
          <strong>{username}</strong>.
        </p>
      ) : (
        <p className="text-red-500 text-center">{message}</p>
      )}

      <div className="flex flex-col gap-5 px-10">
        {['Parse Followers', 'Parse Posts', 'Parse Chats'].map((option, index) => (
          <button
            key={index}
            className="rounded-lg px-4 py-2 text-white bg-green-600 hover:bg-green-800"
            onClick={() => handleButtonClick(option)}
            disabled={isLoading}
          >
            {option}
          </button>
        ))}

        {/* Parse All Button */}
        <button
          className="rounded-lg px-4 py-2 text-white bg-green-600 hover:bg-green-800"
          onClick={handleParseAll}
          disabled={isLoading}
        >
          Parse All
        </button>
      </div>

      {isLoading && (
        <p className="text-blue-500 text-center">Wait... the file is getting ready for download.</p>
      )}

      {message && !isLoading && (
        <p className="text-green-500 text-center">{message}</p>
      )}
    </div>
  );
};

export default Stage2;
