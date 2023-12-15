import mediapipe as mp
import cv2

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    for gesture in result.gestures:
        print([category.category_name for category in gesture])

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