import cv2
import numpy as np
import os

def process_frame(frame, num_pixels):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    all_points = []
    for contour in contours:
        all_points.extend(contour)

    if len(all_points) == 0:
        return " ".join([f"{i}:-6.0,-6.0" for i in range(1, num_pixels + 1)])
    np.random.shuffle(all_points)
    selected_points = all_points[:num_pixels]
    pixel_coordinates = ""
    for i, point in enumerate(selected_points, start=1):
        x, y = point[0]
        pixel_coordinates += f"{i}:{x},{y} "

    return pixel_coordinates.strip()  




input_dir = "input"
output_dir = "precess"


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


N = 49


for filename in os.listdir(input_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        
        frame = cv2.imread(os.path.join(input_dir, filename))
        processed_frame = process_frame(frame, N)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        with open(output_path, "w") as file:
            file.write(processed_frame)

        print(f"Processed {filename}")

print("Processing complete.")
