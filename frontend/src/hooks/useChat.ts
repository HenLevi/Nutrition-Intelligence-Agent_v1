import { useState } from "react";
import { sendMessage } from "../api/chat";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);

  const send = async (text: string) => {
    if (!text.trim()) return;

    const newMessages: Message[] = [
      ...messages,
      { role: "user", content: text }
    ];

    setMessages(newMessages);

    const reply = await sendMessage(newMessages);

    setMessages([
      ...newMessages,
      { role: "assistant", content: reply }
    ]);
  };

  return { messages, send };
}
