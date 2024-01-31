# img_output
 
Introduction
---
- This is a Python-based application that allows users to add custom text to images. 
- Users can select an image from their local machine, add location and author text, and then save the modified image.

Features
---
- Input options:
  - Choose an image file from the local machine. (Supports multiple image formats: .jpg, .jpeg, .png, .HEIC)
  - Add custom location and author text to images.
- Image Rotation(if needed)):
  - Rotate the image by 90, 180, or 270 degrees.
- Output: 
  - Normalizes image size and merges provided textual information.
  - Save the customized image to the local machine.

How to Run
---
1. Install necessary libraries
    ```
    pip install opencv-python numpy pillow pillow_heif
    ```

2. Run the program
    ```
    python main.py
    ```
    The application window will open with options to select an image, add text, and choose image orientation.
    