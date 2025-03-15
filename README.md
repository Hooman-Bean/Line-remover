# Line-remover
Technical Diagram Line Removal Tool
This tool automatically removes connecting lines (pipes) from technical diagrams while preserving symbols. It uses image processing techniques to detect and remove lines, ensuring symbols remain intact.

## Approach
### 1. Image Preprocessing
  - The input image is converted to grayscale and binarized using adaptive thresholding to separate foreground (lines and symbols) from the background.

### 2. Symbol Detection
  - Contour Analysis: Symbols are detected as closed shapes with low aspect ratios and larger areas.
  - Morphological Closing: Ensures symbols are grouped as single entities, even if they contain gaps.

### 3. Line Detection
  - Straight Lines: Detected using the Hough Line Transform.
  - Curved Lines: Detected using contour analysis based on aspect ratio and area heuristics.

### 4. Mask Creation
  - A mask is created to mark the locations of lines. Symbol regions are excluded from this mask to avoid accidental removal.

### 5. Inpainting
  - The detected lines are removed using inpainting, which fills the line regions with surrounding background pixels.

## How to Run the Code
### Prerequisites
- Install Python (3.6 or higher).
- Install the required libraries:

```
pip install opencv-python numpy
```
### Steps
 - Clone the repository or download the script:
```
git clone https://github.com/your-repo/technical-diagram-line-removal.git
cd technical-diagram-line-removal
```
- Place your input image (e.g., input.jpg) in the project directory.

- Run the script:
```
python remove_lines.py
```
- The processed image will be saved as output.jpg.

## Libraries Used
- OpenCV (cv2): For image processing tasks like thresholding, contour detection, and inpainting.
- NumPy (numpy): For numerical operations and array manipulations.

## Fine-Tuning Parameters
 The script includes several parameters that can be adjusted for optimal performance:

### 1. Adaptive Thresholding
  - Block Size (11): Adjust for larger or smaller neighborhoods.
  - Constant (2): Increase to make thresholding stricter.

### 2. Morphological Closing
  - Kernel Size ((5,5)): Increase to close larger gaps.
  - Iterations (2): Increase for more aggressive closing.

### 3. Symbol Detection
  - Aspect Ratio (< 5): Adjust to include/exclude more shapes.
  - Area (> 500): Increase to exclude smaller symbols.

### 4. Line Detection
  - Hough Transform:
    - minLineLength: Increase to exclude shorter lines.
    - maxLineGap: Increase to merge closer line segments.

### Curved Lines:
 - Aspect Ratio (> 25): Adjust to include/exclude more curves.
 - Area (200 < area < 5000): Adjust to exclude smaller/larger contours.

### 5. Inpainting
  - inpaintRadius: Increase for thicker lines, decrease for thinner.

## Example
### Input Image
![alt text](https://github.com/Hooman-Bean/Line-remover/blob/main/input.jpg)

### Output Image
![alt text](https://github.com/Hooman-Bean/Line-remover/blob/main/output.jpg)


## Video Explanation & Demo
https://youtu.be/wco63Bk5gN8
