# flask packages for rendering and serving the website
from flask import Response
from flask import Flask
from flask import render_template

# threading to support multiple clients at once
import threading

# input arguments
import argparse

# image handling
import cv2

# output frame will be served on the stream
outputFrame = None

# lock the output frame, if a thread is using it
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# render the index.html and serve the output stream
@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

# get the next image of the video source
# update the output frame
def next_image():

    global outputFrame, lock

    # loop
    while True:

        # read the next frame from the video stream
        frame = cv2.imread("image.png")

        # acquire the lock, set the output frame, and release the lock
        with lock:
            outputFrame = frame.copy()

# encode the output frame as jpg
def generate():

    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop
    while True:

        # wait until the lock is acquired
        with lock:

            # check if the output frame is available, otherwise skip
            if outputFrame is None:
                continue

            # encode the frame in JPG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

# call generate when the client requests it
@app.route("/video_feed")
def video_feed():

    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True, help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    # start a thread that will grab the next image of the video source
    t = threading.Thread(target=next_image, args=())
            
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
		
# release the video stream pointer
