import axios from 'axios';

const run = async () => {
  try {
    const response = await axios.post('http://localhost:5000/chat', {
      message: 'Hello from Axios!'
    });

    console.log('✅ API Response:\n', response.data);
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
};

run();



