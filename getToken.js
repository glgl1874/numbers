const axios = require('axios');

async function getAccessToken() {
  try {
    const response = await axios.post('https://api.imweb.me/v2/auth', {
      key: '91c289e24f2b46b3ca83e2b3b01f0af5f5cda68182',
      secret: '667ffbb34b9133c9a452af',
    });
    console.log('Access Token:', response.data);
  } catch (error) {
    console.error('Error getting access token:', error.response ? error.response.data : error.message);
  }
}

getAccessToken();
