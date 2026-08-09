#!/usr/bin/env python3
"""
Prep a source photo for ASCII conversion:
1. Remove background with rembg
2. Boost local contrast with CLAHE
3. Composite onto pure white background
Outputs: source-prepped.png (grayscale)
"""
import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image

def prep_photo(input_path: str, output_path: str = "source-prepped.png"):
    # Load image
    with open(input_path, "rb") as f:
        input_data = f.read()
    
    # Remove background
    output_data = remove(input_data)
    
    # Load as RGBA
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    arr = np.array(img)
    
    # Separate alpha and RGB
    alpha = arr[:, :, 3] / 255.0
    rgb = arr[:, :, :3].astype(float)
    
    # Composite onto white
    white = np.ones_like(rgb) * 255
    composited = (rgb * alpha[:, :, None] + white * (1 - alpha[:, :, None])).astype(np.uint8)
    
    # Convert to grayscale
    gray = cv2.cvtColor(composited, cv2.COLOR_RGB2GRAY)
    
    # Apply CLAHE for local contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Save
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped image to {output_path}")

if __name__ == "__main__":
    import io
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py source-photo.jpg")
        sys.exit(1)
    prep_photo(sys.argv[1])