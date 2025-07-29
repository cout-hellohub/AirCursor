import cv2
import math
import mediapipe as mp
import pyautogui
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
screen_width, screen_height = pyautogui.size()

#constants
SCALING_MULTIPLIER = 2.3    #1.5-3.0
SMOOTHING = 0.6             #0.2 - 1.5
prev_x, prev_y = 0, 0
prev_scroll_y = None
SCROLL_SENSITIVITY = 4000    #50-200
click_triggered = False
left_hand_landmarks, right_hand_landmarks = None, None


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands = 2, 
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7,
    model_complexity = 0
    )

def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    fingers = []
    
    # Tip y < pip y means finger is up (except thumb)
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            fingers.append(1)
        else : fingers.append(0)
        
    return fingers      #[index, middle, ring, pinky]

def get_distance(lm1, lm2):
    return math.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)

while True:
    
    #if cv2.getWindowProperty("Hand Tracking - Phase 1", cv2.WND_PROP_VISIBLE) < 1:
    #    break
    
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_idx, hand_landmark in enumerate(result.multi_hand_landmarks):
            hand_label = result.multi_handedness[hand_idx].classification[0].label
            
            if hand_label == "Left":
                left_hand_landmarks = hand_landmark
            elif hand_label == "Right":
                right_hand_landmarks = hand_landmark
            
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            
            lm_list = hand_landmark.landmark
            finger_status = fingers_up(hand_landmark)
            
            if hand_label == "Right":
            # check for index up
                if finger_status == [1,0,0,0]:
                    index_tip = lm_list[8]
                    x = int(index_tip.x * w)
                    y = int(index_tip.y * h)
                    
                    #convert to screen size
                    #screen_x = int(index_tip.x * screen_width)
                    #screen_y = int(index_tip.y * screen_height)
                    
                    dx = (index_tip.x - 0.5) * SCALING_MULTIPLIER
                    dy = (index_tip.y - 0.5) * SCALING_MULTIPLIER
                    
                    screen_x = int((0.5 + dx) * screen_width)
                    screen_y = int((0.5 + dy) * screen_height)
                    
                    screen_x = max(0, min(screen_width - 1, screen_x))
                    screen_y = max(0, min(screen_height - 1, screen_y))
                    
                    #pyautogui.moveTo(screen_x, screen_y)
                    if abs(screen_x - prev_x) > 3 or abs(screen_y - prev_y) > 3:
                        smooth_x = prev_x + (screen_x - prev_x) * SMOOTHING
                        smooth_y = prev_y + (screen_y - prev_y) * SMOOTHING
                        pyautogui.moveTo(int(smooth_x), int(smooth_y))
                        
                        prev_x, prev_y = smooth_x, smooth_y                
                    
                    cv2.putText(frame, "Pointer Mode", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)
                
                if finger_status == [1,1,0,0]:
                    y1 = lm_list[8].y
                    y2 = lm_list[12].y
                    avg_y = (y1 + y2) / 2
                    
                    if prev_scroll_y is not None:
                        delta = (avg_y - prev_scroll_y) * SCROLL_SENSITIVITY
                        #clamp delta
                        #delta = max(-5, min(5, delta))
                        pyautogui.scroll(int(delta))
                    prev_scroll_y = avg_y
                    
                    cv2.putText(frame, "Scroll Mode", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 0), 2)
                else:
                    prev_scroll_y = None
            
            elif hand_label == "Left":
                if finger_status == [0,0,0,0]:
                    if not click_triggered:
                        pyautogui.click()
                        click_triggered = True
                        cv2.putText(frame, "Click!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255), 2)
                else:
                    click_triggered = False
    
    if left_hand_landmarks and right_hand_landmarks:
        left_tip = left_hand_landmarks.landmark[8]
        right_tip = right_hand_landmarks.landmark[8]  
        
        distance = get_distance(left_tip, right_tip)
        
        if distance < 0.05:
            print("Gesture EXIT...")
            break   
    
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27: #ESC to quit
        break
    #if cv2.getWindowProperty("Hand Tracking - Phase 1", cv2.WND_PROP_VISIBLE) < 1:
    #    break

cap.release()
cv2.destroyAllWindows()

