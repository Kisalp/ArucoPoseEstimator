import numpy as np
import cv2
import cv2.aruco as arc
import rclpy

# Global değişkenler
arucoType = arc.DICT_ARUCO_ORIGINAL
arucoDict = arc.getPredefinedDictionary(arucoType)
cam_ins = np.array(((933.15867, 0, 657.59), (0, 933.1586, 400.36993), (0, 0, 1)))
cam_dis = np.array((-0.43948, 0.18514, 0, 0))

def aruco_display(corners, ids, image):
    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners.astype(int)
            cv2.line(image, tuple(topLeft), tuple(topRight), (0, 255, 0), 2)
            cv2.line(image, tuple(topRight), tuple(bottomRight), (0, 255, 0), 2)
            cv2.line(image, tuple(bottomRight), tuple(bottomLeft), (0, 255, 0), 2)
            cv2.line(image, tuple(bottomLeft), tuple(topLeft), (0, 255, 0), 2)
            cX, cY = int((topLeft[0] + bottomRight[0]) / 2.0), int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(f"[Inference] ArUco marker ID: {markerID}")
    return image

def pose_estimation(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected_img_points = arc.detectMarkers(gray, arucoDict)
    aruco_display(corners, ids, frame)
    if len(corners) > 0:
        for i in range(len(ids)):
            rvec, tvec, _ = arc.estimatePoseSingleMarkers(corners[i], 0.02, cam_ins, cam_dis)
            arc.drawDetectedMarkers(frame, corners) 
            cv2.drawFrameAxes(frame, cam_ins, cam_dis, rvec, tvec, 0.01)
    return frame

def main(args=None):
    rclpy.init(args=args)
    cap = cv2.VideoCapture(0)  # Kamera açılıyor
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    try:
        while cap.isOpened():
            ret, image_catch = cap.read()
            if not ret:
                print("Kameradan görüntü alınamadı!")
                break
            output = pose_estimation(image_catch)
            cv2.imshow("Magic", output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
