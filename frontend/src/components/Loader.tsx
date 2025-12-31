import MessageBubble from "./MessageBubble.tsx";

export default function MessageList({ messages }: { messages: any[] }) {
  return (
    <div className="w-full max-w-xl bg-white shadow p-4 rounded-xl flex-1 overflow-y-auto mb-4">
      {messages.map((msg, i) => (
        <MessageBubble key={i} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}
