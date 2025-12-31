import { useState } from "react";

interface InputBarProps {
  onSend: (msg: string) => void;
}

export default function InputBar({ onSend }: InputBarProps) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  const handleKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="flex items-center gap-3 p-4">
      <input
        type="text"
        value={text}
        onKeyDown={handleKey}
        onChange={(e) => setText(e.target.value)}
        className="flex-1 px-4 py-3 rounded-full border border-gray-300"
        placeholder="Type your message..."
      />

      <button
        onClick={handleSend}
        className="px-6 py-3 bg-green-500 text-white rounded-full"
      >
        Send
      </button>
    </div>
  );
}
