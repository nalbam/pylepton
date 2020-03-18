#!/usr/bin/env python3

"""
  This example is for Raspberry Pi (Linux) only!
  It will not work on microcontrollers running CircuitPython!
"""

import cv2
import math
import numpy as np
import os
import pygame
import time
import time
import traceback

from colour import Color

from scipy.interpolate import griddata

from pylepton.Lepton3 import Lepton3


FRAME_RATE = 15

# low range of the sensor (this will be blue on the screen)
MINTEMP = 22.0
MINCOLOR = "indigo"

# high range of the sensor (this will be red on the screen)
MAXTEMP = 40.0
MAXCOLOR = "red"

# how many color values we can have
COLORDEPTH = 1024


# some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def run():
    os.putenv("SDL_FBDEV", "/dev/fb1")

    pygame.init()
    clock = pygame.time.Clock()

    # # initialize the sensor
    # sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

    device = "/dev/spidev0.0"

    a = np.zeros((240, 320, 3), dtype=np.uint8)
    lepton_buf = np.zeros((120, 160, 1), dtype=np.uint16)

    pixels = [160, 120]
    length = pixels[0] * pixels[1]

    # pylint: disable=invalid-slice-index
    points = [(math.floor(ix / pixels[1]), (ix % pixels[1])) for ix in range(0, length)]
    grid_x, grid_y = np.mgrid[0:159:160j, 0:119:120j]
    # pylint: enable=invalid-slice-index

    # sensor is an 8x8 grid so lets do a square
    width = pixels[0] * 4
    height = pixels[1] * 4

    # the list of colors we can choose from
    colors = list(Color(MINCOLOR).range_to(Color(MAXCOLOR), COLORDEPTH))

    # create the array of colors
    colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

    displayPixelWidth = 3
    displayPixelHeight = 3

    screen = pygame.display.set_mode((width, height))

    screen.fill((255, 0, 0))
    pygame.display.update()

    pygame.mouse.set_visible(False)

    screen.fill((0, 0, 0))
    pygame.display.update()

    # let the sensor initialize
    # time.sleep(0.1)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            run = False

        if run == False:
            break

        # read the pixels
        pixels = []

        # # for row in sensor.pixels:
        # #     pixels = pixels + row
        # for temp in range(0, length):
        #     pixels.append(MINTEMP + ((MAXTEMP - MINTEMP) * (temp / length)))

        # pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

        # # perform interpolation
        # bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")

        try:
            # time.sleep(0.2)  # give the overlay buffers a chance to initialize

            with Lepton3(device) as l:
                _, nr = l.capture(lepton_buf)

                print(nr)
                print(len(lepton_buf), len(lepton_buf[0]))

                print(lepton_buf[0][0], lepton_buf[50][50], lepton_buf[100][100])

                cv2.normalize(lepton_buf, lepton_buf, 0, 65535, cv2.NORM_MINMAX)
                np.right_shift(lepton_buf, 8, lepton_buf)

                print(lepton_buf[0][0], lepton_buf[50][50], lepton_buf[100][100])
                print(min(lepton_buf), max(lepton_buf))

                # last_nr = 0
                # while True:
                #     _, nr = l.capture(lepton_buf)
                #     if nr == last_nr:
                #         # no need to redo this frame
                #         continue
                #     last_nr = nr

                #     cv2.normalize(lepton_buf, lepton_buf, 0, 65535, cv2.NORM_MINMAX)
                #     np.right_shift(lepton_buf, 8, lepton_buf)
                #     a[: lepton_buf.shape[0], : lepton_buf.shape[1], :] = lepton_buf

                #     print(len(a))

                #     # o.update(np.getbuffer(a))

        except Exception:
            traceback.print_exc()
        finally:
            print("")

        # draw everything
        for ix, row in enumerate(lepton_buf):
            for jx, pixel in enumerate(row):
                # print(ix, jx, pixel)

                pygame.draw.rect(
                    screen,
                    colors[constrain(int(pixel), 0, COLORDEPTH - 1)],
                    (
                        displayPixelHeight * ix,
                        displayPixelWidth * jx,
                        displayPixelHeight,
                        displayPixelWidth,
                    ),
                )

        pygame.display.update()
        clock.tick(FRAME_RATE)

    pygame.quit()


run()
