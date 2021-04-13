import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def process_hands(hands, image, tip_ids):
    results = hands.process(image)
    fingers = []
    for multi_landmark in results.multi_hand_landmarks:
        fingers = []
        # thumb
        thumb_tip = multi_landmark.landmark[tip_ids[0]].x * image.shape[0]
        thumb_pip = multi_landmark.landmark[tip_ids[0] - 1].x * image.shape[0]
        if (thumb_tip < thumb_pip):
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for idx in range(1, 5):
            tip = multi_landmark.landmark[tip_ids[idx]].y * image.shape[1]
            pip = multi_landmark.landmark[tip_ids[idx] - 2].y * image.shape[1]
            if (int(tip) < int(pip)):
                fingers.append(1)
            else:
                fingers.append(0)
    return results, fingers


def hand_detect(image):
    tip_ids = [4, 8, 12, 16, 20]
    hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
    results, fingers = process_hands(hands, image, tip_ids)
    return results, fingers