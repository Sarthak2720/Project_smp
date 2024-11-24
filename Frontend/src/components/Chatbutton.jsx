import React from 'react'
import { Link } from 'react-router-dom'

const Chatbutton = () => {
  return (
    <Link to='/chatbot' className='absolute bottom-20 right-20 chatbot-btn px-3 py-2 rounded-lg bg-green-500 text-white font-semibold'>
      Chatbot 🤖
    </Link>
  )
}

export default Chatbutton
