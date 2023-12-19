import mediapipe as mp
import cv2
import subprocess as sp
import pyautogui

url = "http://192.168.0.102:8080/video"

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(url)
counter1 = {'stop': 0, 'one': 0, 'fist': 0}
counter2 = {'stop': True, 'one': True, 'fist': True}
period = 5

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    for gesture in result.gestures:
        pose = str([category.category_name for category in gesture].pop())
        work(pose)


def work(pose):
    if pose == "stop":
        counter1['stop'] += 1
        if counter1['stop'] == period and counter2['stop']:
            print("open notepad")
            programName = "notepad.exe"
            fileName = "sample.txt"
            sp.Popen([programName, fileName])
            counter1['stop'] = 0
            counter2['stop'] = False

    elif pose == "fist":
        counter1['fist'] += 1
        if counter1['fist'] == period and counter2['fist']:
            print("close notepad")
            sp.call("TASKKILL /F /IM notepad.exe", shell=True)
            counter1['fist'] = 0
            counter2['fist'] = False

    elif pose == "one":
        counter1['one'] += 1
        if counter1['one'] == period and counter2['one']:
            print("Print Done")
            pyautogui.write('Done')
            counter1['one'] = 0
            counter2['one'] = False

def show(frame):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("output", 600, 600)
    cv2.imshow("output", frame)

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