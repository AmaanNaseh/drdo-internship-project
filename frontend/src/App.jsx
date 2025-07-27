import { backendAPI } from "./config/Config";

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-4">
        Red Box Detection Using AI Algorithm
      </h1>
      <img
        src={`${backendAPI}/video_feed`}
        alt="Object Detection Stream"
        className="border-4 border-green-500 rounded min-w-[300px] md:min-w-[500px] min-h-[300px] md:min-h-[500px]"
      />
    </div>
  );
}

export default App;
