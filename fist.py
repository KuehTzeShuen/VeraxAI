import cv2
import mediapipe as mp


def cameravision():
    # 0 is your built-in webcam
    # 1 is an external webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # New for finger detection
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    try:
        while 1:

            font = cv2.FONT_HERSHEY_SIMPLEX
            ret, frame = cap.read()
            # New for finger detection
            handsFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(handsFrame)

            if results.multi_hand_landmarks:
                for handLMS in results.multi_hand_landmarks:
                    # https://google.github.io/mediapipe/solutions/hands.html
                    # mpDraw.draw_landmarks(handsFrame, handLMS, mpHands.HAND_CONNECTIONS)
                    lmList = []
                    for id, lm in enumerate(handLMS.landmark):
                        h, w, c = handsFrame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                        # use landmark map to identify the point you want to highlight
                        # if id == 12:
                            # cv2.circle(handsFrame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    indexX = 0
                    indexY = 0
                    indexMid = 0
                    handBottomX = 0
                    handBottomY = 0
                    pinkyX = 0
                    pinkyY = 0
                    fistWarning = "Fist!"
                    for lms in lmList:
                        if lms[0] == 7:
                            indexX, indexY = lms[1], lms[2]
                            # cv2.circle(handsFrame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 5:
                            indexMid = lms[2]
                        # elif lms[0] == 11:
                            # middleY = lms[2]
                            # cv2.circle(handsFrame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                        # elif lms[0] == 15:
                            # ringY = lms[2]
                            # cv2.circle(handsFrame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 19:
                            pinkyX, pinkyY = lms[1], lms[2]
                            # cv2.circle(handsFrame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 0:
                            handBottomX, handBottomY = lms[1], lms[2]
                    if (indexY < handBottomY) and (indexY > indexMid):
                        cv2.rectangle(handsFrame, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                        cv2.putText(handsFrame, fistWarning, (pinkyX + 2, indexY - 2), (font), .7,
                                    (0, 0, 255), 1, cv2.LINE_4)
                        print("Fist!!")

            cv2.imshow("Your Project", handsFrame)

            k = cv2.waitKey(10) & 0xFF
            #  27 is the escape key
            if k == 27:
                break
            else:
                pass

        cap.release()

        cv2.destroyAllWindows()

    except cv2.error as e:
        print(str(e))


cameravision()
