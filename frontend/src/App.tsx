import Chat from "./components/Chat";
import logo from "../public/logo.png";

export default function App() {
  return (
    <div className="min-h-screen bg-[#f5f6f8] flex justify-center p-6">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-lg border flex flex-col">

        {/* HEADER */}
        <div className="text-center py-6">
          <img src={logo} alt="logo" className="w-16 mx-auto mb-2" />
          <h1 className="text-3xl font-semibold">Nutrition Intelligence Agent</h1>
          <div className="w-32 h-1 bg-green-500 mx-auto mt-2 rounded"></div>
        </div>

        <div className="flex-1">
          <Chat />
        </div>
      </div>
    </div>
  );
}
