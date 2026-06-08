import cv2
import mediapipe as mp
import keyboard
import time
import math
import webbrowser

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Open the Subway Surfers web game
print("Opening the game website in your browser...")
webbrowser.open('https://poki.com/en/g/subway-surfers')
time.sleep(3) # Give the browser a few seconds to load

# Video capture
# cv2.CAP_DSHOW is highly recommended on Windows for reliable camera access
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("\n[!] ERROR: Could not open the webcam (index 0).")
    print("[!] Make sure your camera is connected and not being used by another app (like Zoom).")
    print("[!] Also check Windows Privacy Settings -> Camera -> 'Let desktop apps access your camera'.\n")
    time.sleep(10) # Pause so you can read the error
    exit()

# Gesture state variables
cooldown_time = 0.0 # Removed all cooldown for maximum speed
last_action_time = 0
prev_finger_count = 0 # To prevent spamming finger-based gestures

# Stability tracking
current_finger_count = 0
frames_stable = 0
prev_wrist_x, prev_wrist_y = 0, 0 # To track hand movement speed
prev_rel_tips = None # To track finger morphing speed

print("Hand Gesture Controller for Subway Surfers Started!")
print("Bring your hand into the frame.")

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("[!] ERROR: Failed to read video frame. The camera might have disconnected.")
        time.sleep(5)
        break

    # Flip the image horizontally for a selfie-view display
    img = cv2.flip(img, 1)
    
    # Convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect hands
    results = hands.process(img_rgb)
    
    current_time = time.time()
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract landmark positions
            h, w, c = img.shape
            landmarks = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([id, cx, cy])
            
            if landmarks:
                # Use the Middle Finger MCP (knuckle) for tracking movement
                # It is a stable point on the hand
                curr_x, curr_y = landmarks[9][1], landmarks[9][2]
                
                # Draw a circle on the tracking point
                cv2.circle(img, (curr_x, curr_y), 15, (255, 0, 255), cv2.FILLED)

                # 1. Check for Static Finger Gestures
                wrist = landmarks[0]
                
                # Calculate hand speed to prevent motion blur false-positives
                curr_wrist_x, curr_wrist_y = wrist[1], wrist[2]
                if prev_wrist_x != 0:
                    hand_speed = math.hypot(curr_wrist_x - prev_wrist_x, curr_wrist_y - prev_wrist_y)
                else:
                    hand_speed = 0
                prev_wrist_x, prev_wrist_y = curr_wrist_x, curr_wrist_y
                
                # If hand is moving wildly fast, it creates motion blur. Ignore it until it slows down.
                if hand_speed > 30:
                    frames_stable = 0
                    continue
                    
                # Calculate Morph Speed (speed of fingertips relative to the wrist)
                curr_rel_tips = {}
                max_morph_speed = 0
                for i in [8, 12, 16, 20]:
                    rel_x = landmarks[i][1] - curr_wrist_x
                    rel_y = landmarks[i][2] - curr_wrist_y
                    curr_rel_tips[i] = (rel_x, rel_y)
                    if prev_rel_tips is not None:
                        prev_rel_x, prev_rel_y = prev_rel_tips[i]
                        speed = math.hypot(rel_x - prev_rel_x, rel_y - prev_rel_y)
                        if speed > max_morph_speed:
                            max_morph_speed = speed
                prev_rel_tips = curr_rel_tips
                
                # If fingers are actively extending or folding (changing shape), ignore intermediate states!
                if max_morph_speed > 10:
                    frames_stable = 0
                    continue

                # We check all 5 fingers. 
                # A finger is "up" if its tip is further from the wrist than its lower joint.
                # This makes it work perfectly even if you tilt or rotate your hand!
                def get_dist(lm):
                    return math.hypot(lm[1] - wrist[1], lm[2] - wrist[2])

                fingers_up = 0
                if get_dist(landmarks[8]) > get_dist(landmarks[6]): fingers_up += 1   # Index
                if get_dist(landmarks[12]) > get_dist(landmarks[10]): fingers_up += 1 # Middle
                if get_dist(landmarks[16]) > get_dist(landmarks[14]): fingers_up += 1 # Ring
                if get_dist(landmarks[20]) > get_dist(landmarks[18]): fingers_up += 1 # Pinky
                
                # Stabilize the reading to prevent accidental inputs when opening/closing hand
                if fingers_up == current_finger_count:
                    frames_stable += 1
                else:
                    current_finger_count = fingers_up
                    frames_stable = 1
                
                # Check for actions (require 2 frames of stability to safely allow shifting between arbitrary fingers)
                if frames_stable >= 2 and current_time - last_action_time >= cooldown_time:
                    if fingers_up != prev_finger_count:
                        if fingers_up == 1:
                            print(f"Gesture: {fingers_up} FINGER -> MOVE LEFT (Left Arrow)")
                            keyboard.press_and_release('left')
                        elif fingers_up == 2:
                            print(f"Gesture: {fingers_up} FINGERS -> MOVE RIGHT (Right Arrow)")
                            keyboard.press_and_release('right')
                        elif fingers_up == 3:
                            print(f"Gesture: 3 FINGERS -> SLIDE (Down Arrow)")
                            keyboard.press_and_release('down')
                        elif fingers_up == 4:
                            print(f"Gesture: 5 FINGERS (Open Hand) -> JUMP (Up Arrow)")
                            keyboard.press_and_release('up')
                        last_action_time = current_time
                            
                        # Update previous count to prevent spamming the SAME action, and to reset on fist
                        prev_finger_count = fingers_up

    cv2.imshow("Subway Surfers Controller", img)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
