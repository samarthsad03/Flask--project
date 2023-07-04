from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        ##read the camera frame
        success, frame = camera.read()
        # success is the boolean variable here
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg",frame)
            frame = buffer.tobytes()
        # To go back over there we need to use the kwyword yield instead of return.
        yield (b"--frame\r\n" b"Content-Type: image\jpg\r\n\r\n" + frame + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace;boundary=frame"
    )


# Response will call some function which will be taking some frames from webcam and pass it to back to index.html

if __name__ == "__main__":
    app.run(debug=True)
