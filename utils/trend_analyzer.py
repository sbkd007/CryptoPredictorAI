import numpy as np
from .image_processor import extract_trend_line

def analyze_trends(processed_image):
    """
    Analyze trends for different timeframes from the processed image.
    
    Args:
        processed_image (numpy.ndarray): Processed image array
    
    Returns:
        dict: Analysis results for each timeframe
    """
    height, width = processed_image.shape
    results = {}
    
    # Define timeframes and their corresponding image regions
    timeframes = {
        '5 minutes': (0, 0, width//6, height),
        '10 minutes': (width//6, 0, width//3, height),
        '20 minutes': (width//3, 0, width//2, height),
        '40 minutes': (width//2, 0, 2*width//3, height),
        '1 hour': (2*width//3, 0, 5*width//6, height),
        '1 day': (5*width//6, 0, width, height)
    }
    
    for timeframe, region in timeframes.items():
        # Extract trend line for the region
        slope, confidence = extract_trend_line(processed_image, region)
        
        # Determine trend direction
        direction = "up" if slope < 0 else "down"  # Note: y-axis is inverted in image coordinates
        
        results[timeframe] = {
            'direction': direction,
            'confidence': confidence,
            'slope': slope
        }
    
    return results
