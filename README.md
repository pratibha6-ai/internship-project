
# 🚀 Prompt API Project

Modern full-stack project with a backend API server using Express, integrated via Axios, and proxied through Vite. Designed for fast prototyping, clean architecture, and AI interaction workflows.

---

## 🔧 Tech Stack

- **Backend:** Node.js + Express (ES Module)
- **Frontend:** Vite + React
- **API Client:** Axios
- **Style:** TailwindCSS (via Vite plugin)
- **AI SDK:** @google/generative-ai
- **Others:** Puppeteer, React Icons

---

## 📁 Folder Structure

```
prompt_api_project/
├── backend/              # (Optional logic handlers)
├── node_modules/         
├── public/               
├── src/                  # React Frontend
├── server.mjs            # Express Server Entry (runs on port 5000)
├── fetch_api.js          # Axios test client for API
├── index.html            
├── vite.config.js        # Vite config with API proxying
├── tailwind.config.js    
├── eslint.config.js      
├── package.json          
├── package-lock.json     
└── README.md             
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Start the Backend Server
```bash
node server.mjs
```

### 3. Run Axios API Test
```bash
node fetch_api.js
```

---

## 📡 API Usage

**POST** `http://localhost:5000/chat`  
**Body:**

```json
{
  "message": "Hello from client!"
}
```

**Response:**

```json
{
  "reply": "I'm a code generation assistant and can only help with programming-related requests."
}
```

---

## 🌐 Vite Proxy Config

Requests from the frontend to `/api` are proxied to the Express server on port `5000`:

```js
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

---

## 🙋‍♂️ Author

**Poco** — AI & Robotics Enthusiast  
📧 your-email@example.com  
🌐 GitHub | LinkedIn

---

## 🪪 License

[MIT](LICENSE)
