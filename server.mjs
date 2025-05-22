import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// 🧠 Simple rule-based chatbot logic
function basicBotReply(message) {
  message = message.toLowerCase();
  if (message.includes("hello")) return "Hi there!";
  if (message.includes("how are you")) return "I'm just code, but doing great!";
  if (message.includes("bye")) return "Goodbye!";
  return "I don't understand, but I'm learning!";
}

// 🔁 Chat endpoint (no API key needed)
app.post('/chat', async (req, res) => {
  try {
    const userMessage = req.body.message;
    console.log("📥 User:", userMessage);

    const responseText = basicBotReply(userMessage);
    console.log("📤 Bot:", responseText);

    res.json({ response: responseText });
  } catch (err) {
    console.error("❌ Error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
