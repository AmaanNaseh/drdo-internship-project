import { useRef, useEffect, useState } from "react";
import { backendAPI } from "./config/Config";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [processedImg, setProcessedImg] = useState(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const streamRef = useRef(null); // To store stream for closing

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsCameraOn(true);
      }
    } catch (error) {
      console.error("Error accessing camera:", error);
      alert("Camera access denied or not available.");
    }
  };

  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
      setIsCameraOn(false);
      videoRef.current.srcObject = null;
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (!videoRef.current || !canvasRef.current || !isCameraOn) return;

      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const video = videoRef.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const formData = new FormData();
        formData.append("frame", blob);

        try {
          const res = await fetch(`${backendAPI}/video_feed`, {
            method: "POST",
            body: formData,
          });

          const imageBlob = await res.blob();
          const imageUrl = URL.createObjectURL(imageBlob);
          setProcessedImg(imageUrl);
        } catch (err) {
          console.error("Failed to send frame:", err);
        }
      }, "image/jpeg");
    }, 300);

    return () => clearInterval(interval);
  }, [isCameraOn]);

  return (
    <>
      <div className="flex flex-col items-center justify-center gap-4 m-4 mt-10">
        <h1 className="text-2xl font-bold text-center">
          Red Box Detection Using AI Algorithm
        </h1>

        {!isCameraOn ? (
          <button
            onClick={startCamera}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-500"
          >
            Start Camera
          </button>
        ) : (
          <button
            onClick={closeCamera}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-500"
          >
            Close Camera
          </button>
        )}
      </div>

      <div className="flex flex-col items-center justify-center md:flex-row gap-8 p-4">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="border-4 border-green-500 rounded w-[300px] h-[300px]"
        />

        {/* Hidden canvas for capturing video frame */}
        <canvas ref={canvasRef} style={{ display: "none" }} />

        {processedImg && (
          <img
            src={processedImg}
            alt="Processed Frame"
            className="border-4 border-red-500 rounded w-[300px] h-[300px]"
          />
        )}
      </div>
    </>
  );
}

export default App;
