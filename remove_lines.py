import cv2
import numpy as np

def remove_lines(input_path, output_path):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 3)
    
    # Morphological closing to group symbols
    kernel = np.ones((1,1), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Detect symbols (closed contours with low aspect ratio)
    symbol_mask = np.zeros_like(gray)
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        if hierarchy[0][i][3] != -1:  # Check if contour is inside another (symbols with text)
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = max(w, h) / (min(w, h) + 1e-5)
        area = cv2.contourArea(cnt)
        if aspect_ratio < 10 and area > 300:
            cv2.drawContours(symbol_mask, [cnt], -1, 255, -1)
    
    # Detect lines
    line_mask = np.zeros_like(gray)
    lines = cv2.HoughLinesP(thresh, rho=1, theta=np.pi/180, threshold=50, 
                            minLineLength=50, maxLineGap=3)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_mask, (x1, y1), (x2, y2), 255, 3)
    
    # Detect curved lines (excluding symbols)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = max(w, h) / (min(w, h) + 1e-5)
        area = cv2.contourArea(cnt)
        if aspect_ratio > 25 and 100 < area < 5000:
            cv2.drawContours(line_mask, [cnt], -1, 255, 2)
    
    # Exclude symbol regions from line mask
    line_mask = cv2.bitwise_and(line_mask, cv2.bitwise_not(symbol_mask))

    # Dilate and inpaint
    line_mask = cv2.dilate(line_mask, np.ones((3,3), np.uint8), iterations=2)
    result = cv2.inpaint(img, line_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(output_path, result)

remove_lines("D:\Projects\data\input.jpg", "output.jpg")
