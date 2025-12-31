import { useChat } from "../hooks/useChat";
import InputBar from "./InputBar";
import MessageBubble from "./MessageBubble";

export default function Chat() {
  const { messages, send } = useChat();

  return (
    <div className="flex flex-col h-full">

      {/* CHAT AREA */}
      <div className="flex-1 p-4 overflow-auto space-y-4 bg-white rounded-xl shadow flex flex-col">

        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-gray-500 italic">
            How can I help you improve your nutrition today?
          </div>
        )}

        {messages.map((m, index) => (
          <MessageBubble
            key={index}
            role={m.role}
            content={m.content}
          />
        ))}

      </div>

      <InputBar onSend={send} />
    </div>
  );
}
