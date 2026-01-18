from flask import Flask, Response
import cv2

app = Flask(__name__)

TAPO_RTSP_URL = "rtsp://raghuveer.paturi@gmail.com:Tapo@54321@192.168.1.135:554/stream1x"

@app.route('/')
def index():
    return "Tapo Camera Live Streaming Service is Running!"

@app.route('/stream')
def stream_video():
    camera = cv2.VideoCapture(TAPO_RTSP_URL)
    if not camera.isOpened():
        return "Unable to connect to the camera stream!", 500

    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
