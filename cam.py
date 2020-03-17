#!/usr/bin/env python

import argparse
import cv2
import numpy as np

from pylepton.Lepton3 import Lepton3


def parse_args():
    p = argparse.ArgumentParser(description="webcam demo")
    p.add_argument("--camera-id", type=int, default=0, help="camera id")
    p.add_argument("--device", default="/dev/spidev0.0", help="device")
    p.add_argument("--full-screen", action="store_true", help="full screen")
    p.add_argument("--mirror", action="store_true", help="mirror")
    p.add_argument("--height", type=int, default=0, help="height")
    p.add_argument("--width", type=int, default=0, help="width")
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

    a = np.zeros((240, 320, 3), dtype=np.uint8)
    lepton_buf = np.zeros((120, 160, 1), dtype=np.uint16)

    while True:
        # Grab a single frame of video
        ret, frame = cap.read()

        if args.mirror:
            # Invert left and right
            frame = cv2.flip(frame, 1)

        overlay = frame.copy()

        try:
            time.sleep(0.2)  # give the overlay buffers a chance to initialize
            with Lepton3(args.device) as l:
                last_nr = 0
                while True:
                    _, nr = l.capture(lepton_buf)
                    if nr == last_nr:
                        # no need to redo this frame
                        continue
                    last_nr = nr
                    cv2.normalize(lepton_buf, lepton_buf, 0, 65535, cv2.NORM_MINMAX)
                    np.right_shift(lepton_buf, 8, lepton_buf)
                    a[: lepton_buf.shape[0], : lepton_buf.shape[1], :] = lepton_buf
                    o.update(np.getbuffer(a))
        except Exception:
            traceback.print_exc()
        finally:
            cv2.imshow("Video", overlay)

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
