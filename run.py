import os
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import re

# Function to crop the top 20% of the image
def crop_image(image_path, output_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    crop_height = int(height * 0.2)
    cropped_img = img[crop_height:, :]
    cv2.imwrite(output_path, cropped_img)
    return output_path

# Function to clean the image using OpenCV
def clean_image(image_path, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    denoised_image = cv2.medianBlur(binary_image, 3)
    cv2.imwrite(output_path, denoised_image)
    return output_path

# Function to preprocess the image for OCR
def preprocess_image(image_path):
    image = Image.open(image_path)
    gray_image = image.convert("L")
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    threshold_image = enhanced_image.point(lambda x: 0 if x < 128 else 255)
    return threshold_image

# Function to extract numbers using Tesseract OCR
def extract_numbers(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image, config="--psm 6")
    numbers = re.findall(r'\d+', text)
    return numbers

# Main process
def main():
    # Paths
    original_image = "screen.png"
    os.system(f"adb exec-out screencap -p > {original_image}")
    print("Screenshot saved as 'screen.png'")
    cropped_image = "cropped_image.png"
    cleaned_image = "cleaned_image.png"

    # Step 1: Crop the top 20% of the image
    cropped_image = crop_image(original_image, cropped_image)

    # Step 2: Clean the image
    cleaned_image = clean_image(cropped_image, cleaned_image)

    # Step 3: Extract numbers from the cleaned image
    numbers = extract_numbers(cleaned_image)

    # Join numbers if the list length is 1, 2, or 3
    if 1 <= len(numbers) <= 3:
        concatenated = ''.join(numbers)
        numbers.append(concatenated)  # Add the concatenated string to the list

    # Print results
    print("Updated Extracted Numbers:", numbers)

# Run the main process
if __name__ == "__main__":
    main()
