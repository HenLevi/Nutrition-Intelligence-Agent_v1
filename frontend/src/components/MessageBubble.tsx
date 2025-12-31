export default function MessageBubble({
  role,
  content,
}: {
  role: "assistant" | "user";
  content: string;
}) {
  const isHebrew = /[\u0590-\u05FF]/.test(content);
  const isUser = role === "user";

  // קובעים יישור לפי שפה + role
  const alignment = isHebrew
    ? isUser
      ? "self-end"   // עברית – user מימין
      : "self-start" // עברית – assistant משמאל
    : isUser
      ? "self-end"   // אנגלית – user מימין
      : "self-start";

  return (
    <div
      dir={isHebrew ? "rtl" : "ltr"}
      className={`message-bubble max-w-[80%] px-4 py-2 mb-2 rounded-2xl text-sm shadow-sm ${alignment} ${
        isUser
          ? "bg-green-200 text-gray-900"
          : "bg-blue-100 text-gray-800"
      }`}
    >
      {content}
    </div>
  );
}
