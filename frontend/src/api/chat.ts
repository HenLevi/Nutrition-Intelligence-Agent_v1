

export type Role = "user" | "assistant";

export interface Message {
  role: Role;
  content: string;
}

export async function sendMessage(messages: Message[]): Promise<string> {
  try {
    const res = await fetch("http://localhost:8000/rag-chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ messages }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    return data.reply ?? "No reply from server.";
  } catch (err) {
    console.error("sendMessage error:", err);
    return "Network error. Please try again later.";
  }
}


