import cv2
import numpy as np

def process_image(image):
    """
    Process the input image for trend analysis.
    
    Args:
        image (numpy.ndarray): Input image array
    
    Returns:
        numpy.ndarray: Processed image ready for analysis
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Apply dilation to connect edges
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)

    return dilated

def extract_trend_line(processed_image, region):
    """
    Extract trend line from a specific region of the processed image.
    
    Args:
        processed_image (numpy.ndarray): Processed image
        region (tuple): Region coordinates (x1, y1, x2, y2)
    
    Returns:
        tuple: Slope and confidence of the trend line
    """
    x1, y1, x2, y2 = region
    roi = processed_image[y1:y2, x1:x2]
    
    # Find lines using Hough transform
    lines = cv2.HoughLinesP(roi, 1, np.pi/180, threshold=50, 
                           minLineLength=20, maxLineGap=10)
    
    if lines is None:
        return 0, 0
    
    # Calculate average slope
    slopes = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            slopes.append(slope)
    
    if not slopes:
        return 0, 0
    
    avg_slope = np.mean(slopes)
    confidence = min(100, len(slopes) * 10)  # Simple confidence calculation
    
    return avg_slope, confidence
