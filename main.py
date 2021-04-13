import cv2
import mediapipe as mp
from util.HandDetection import hand_detect
from ppt_access import access_ppt

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
def run():
    cap = cv2.VideoCapture(0)
    prev_number = 0
    presentation = access_ppt.run()
    if(presentation == -1):
        return 0
    while cap.isOpened():
        fingers = []
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        try:
            results, fingers = hand_detect(image)
        except:
            pass
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        except:
            pass
        cv2.putText(image, str(sum(fingers)), (0, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Access Powerpoint', image)
        if(sum(fingers) != prev_number):
            # Access PPT
            print(sum(fingers))
            return_value = access_ppt.nextslide(presentation, sum(fingers))
            prev_number = sum(fingers)
            if (return_value == -1):
                break
        else:
            # do not access PPT
            prev_number = sum(fingers)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cv2.destroyWindow('Access Powerpoint')
    cap.release()

if __name__ == '__main__':
    run()
