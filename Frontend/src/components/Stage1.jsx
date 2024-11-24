import { CheckCircle2, Eye, EyeOff, User, CheckCircle } from 'lucide-react';
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const Stage1 = () => {
  const { platform } = useParams(); // Get the platform from URL
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordType, setPasswordType] = useState('password');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false); // New state for success modal
  const navigate = useNavigate();

  // Toggle password visibility
  const togglePasswordVisibility = () => {
    setPasswordType(passwordType === 'password' ? 'text' : 'password');
  };

  const handleLogin = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      // Sending the login data (platform, username, password) to the backend
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ platform, username, password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setShowSuccess(true); // Show success message

        // Save credentials in session storage (for later use)
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('password', password);
        sessionStorage.setItem('platform', platform);

        // Automatically navigate to the next page after 2 seconds
        setTimeout(() => {
          navigate('/stage2');
        }, 2000);
      } else {
        setErrorMessage(data.message || 'Invalid username or password');
      }
    } catch (error) {
      setErrorMessage('An error occurred while logging in. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative">
      {/* Login Form */}
      <div className="loginContainer h-[60vh] flex flex-col gap-10 rounded-md w-[25vw] border-2 border-black bg-white">
        <div className="flex justify-evenly p-6">
          <CheckCircle2 className="bg-green-500 rounded-full" />
          <p className="rounded-full border border-black px-2 py-1">2</p>
          <p className="rounded-full border border-black px-2 py-1">3</p>
        </div>

        <h1 className="text-3xl text-center font-medium">
          {`Login to ${platform.charAt(0).toUpperCase() + platform.slice(1)}`}
        </h1>

        <div className="flex justify-center items-center relative">
          <User className="absolute right-24" />
          <input
            type="text"
            className="rounded-lg border px-3 py-2 border-neutral-300"
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="flex justify-center items-center relative">
          <button
            type="button"
            className="absolute top-0 right-24 p-2"
            onClick={togglePasswordVisibility}
          >
            {passwordType === 'password' ? <Eye /> : <EyeOff />}
          </button>
          <input
            type={passwordType}
            className="rounded-lg border px-3 py-2 border-neutral-300"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {errorMessage && <p className="text-red-500 text-center">{errorMessage}</p>}

        <div className="flex justify-center">
          <button
            className="hover:no-underline bg-green-500 rounded-md px-3 py-2 w-20 flex justify-center items-center"
            onClick={handleLogin}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Login'}
          </button>
        </div>
      </div>

      {/* Success Message Overlay */}
      {showSuccess && (
        <div className="absolute inset-0 flex justify-center items-center bg-black bg-opacity-50">
          <div className="flex flex-col items-center bg-white rounded-lg p-8 shadow-lg w-[30vw]">
            <CheckCircle className="text-green-500 w-16 h-16" />
            <h2 className="text-2xl font-semibold text-green-500 mt-4">
              Login Successful!
            </h2>
            <p className="text-gray-500 mt-2">
              Redirecting you to the next stage...
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Stage1;
