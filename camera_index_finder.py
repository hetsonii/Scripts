import cv2

def find_camera_index():
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            cap.release()
            index += 1
            if index >= 10:  # Adjust this value based on the maximum number of devices you expect
                return None  
        else:
            cap.release()
            return index

camera_index = find_camera_index()
if camera_index is not None:
    print(f"Camera found at index {camera_index}")
else:
    print("No camera found")
