# import the necessary packages
import argparse
import cv2

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True, help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32, help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    print("Exit with ESC!!!")

    frame = cv2.imread("image.png")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
