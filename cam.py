#!/usr/bin/env python

import argparse
import cv2
import numpy as np


def parse_args():
    p = argparse.ArgumentParser(description="webcam demo")
    p.add_argument("--camera-id", type=int, default=0, help="camera id")
    p.add_argument("--full-screen", action="store_true", help="full screen")
    p.add_argument("--mirror", action="store_true", help="mirror")
    p.add_argument("--width", type=int, default=0, help="width")
    p.add_argument("--height", type=int, default=0, help="height")
    p.add_argument("--crop", action="store_true", help="crop")
    p.add_argument("--mosaic", action="store_true", help="mosaic")
    return p.parse_args()


def main():
    args = parse_args()

    # Get a reference to webcam #0 (the default one)
    cap = cv2.VideoCapture(args.camera_id)

    if args.width > 0 and args.height > 0:
        frame_w = args.width
        frame_h = args.height
    else:
        frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(frame_w, frame_h)
    print('Press "Esc", "q" or "Q" to exit.')

    while True:
        # Grab a single frame of video
        ret, frame = cap.read()

        if args.mirror:
            # Invert left and right
            frame = cv2.flip(frame, 1)

        # print("Resolution: " + str(frame.shape[0]) + " x " + str(frame.shape[1]))

        if args.crop:
            w = int(frame_w / 2)
            x = int((frame_w - w) / 2)
            y = int((frame_h - w) / 2)

            # Crop square
            frame = frame[y : y + w, x : x + w]

        if args.mosaic:
            rate = 8 / frame_h
            bigg = frame_h / 8

            # Resize to 8x8
            frame = cv2.resize(frame, (0, 0), fx=rate, fy=rate)

            # Resize to orignal
            frame = cv2.resize(
                frame, (0, 0), fx=bigg, fy=bigg, interpolation=cv2.INTER_AREA
            )

        # Display the resulting image
        cv2.imshow("Video", frame)

        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)

        if args.full_screen:
            cv2.setWindowProperty(
                "Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
            )

        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord("q") or ch == ord("Q"):
            break

    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
