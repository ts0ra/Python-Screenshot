import os
os.add_dll_directory("C:/gstreamer/1.0/msvc_x86_64/bin") # Gstreamer_bin_path is the path to the bin folder of Gstreamer
import cv2
import win32api
import win32con
import win32gui
import win32ui
import time
import numpy as np

def capture_screen():
    # Get the dimensions of the primary monitor
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    # Calculate the coordinates for the 640x640 region in the middle of the screen
    region_width = 640
    region_height = 640
    region_left = (screen_width - region_width) // 2
    region_top = (screen_height - region_height) // 2

    # Create a device context for the entire screen
    screen_dc = win32gui.GetDC(0)
    screen_dc_compat = win32ui.CreateDCFromHandle(screen_dc)

    # Create a compatible DC
    memory_dc = screen_dc_compat.CreateCompatibleDC()

    # Create a bitmap that will hold the screenshot
    screenshot_bitmap = win32ui.CreateBitmap()
    screenshot_bitmap.CreateCompatibleBitmap(screen_dc_compat, region_width, region_height)
    memory_dc.SelectObject(screenshot_bitmap)

    # Capture the screen region
    memory_dc.BitBlt((0, 0), (region_width, region_height), screen_dc_compat, (region_left, region_top), win32con.SRCCOPY)

    image = np.frombuffer(screenshot_bitmap.GetBitmapBits(True), dtype=np.uint8).reshape((region_height, region_width, 4))

    # Clean up
    win32gui.DeleteObject(screenshot_bitmap.GetHandle())
    screen_dc_compat.DeleteDC()
    memory_dc.DeleteDC()
    win32gui.ReleaseDC(0, screen_dc)

    return image


# Calculate FPS
frame_count = 0
start_time = time.time()

while True:
    # Capture the entire screen
    screenshot = capture_screen()

    # Display the screenshot using OpenCV
    cv2.imshow("Screenshot", screenshot)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update frame count and calculate FPS
    frame_count += 1
    if frame_count % 15 == 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = frame_count / elapsed_time
        print(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.time()

cv2.destroyAllWindows()