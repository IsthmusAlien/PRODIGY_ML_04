import mediapipe as mp
import cv2
import subprocess as sp
import pyautogui

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)
counter = {'stop': 0, 'two_up': 0, 'fist': 0}
period = 60

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    for gesture in result.gestures:
        pose = str([category.category_name for category in gesture].pop())
        work(pose)


def work(pose):
    if pose == "stop":
        counter['stop'] += 1
        if counter['stop'] == period:
            programName = "notepad.exe"
            fileName = "sample.txt"
            sp.Popen([programName, fileName])
            counter['stop'] = 0

    elif pose == "fist":
        counter['fist'] += 1
        if counter['fist'] == period:
            sp.call("TASKKILL /F /IM notepad.exe", shell=True)
            counter['fist'] = 0

    elif pose == "two_up":
        counter['two_up'] += 1
        if counter['two_up'] == period:
            pyautogui.write('Done')
            counter['two_up'] = 0

def show(frame):
    cv2.imshow("FEED", frame)

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='model4.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
    while video.isOpened():

        _, frame = video.read()

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        recognizer.recognize_async(mp_image, timestamp)

        show(frame)

        k = cv2.waitKey(1)
        if k == ord("q"):
            break

video.release()
cv2.destroyAllWindows()