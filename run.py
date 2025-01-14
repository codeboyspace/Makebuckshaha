import os
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import re

# Function to crop the top 20% of the image
def crop_image(image_path, output_path):
    # Load the image
    img = cv2.imread(image_path)

    # Calculate the cropping dimensions
    height, width = img.shape[:2]
    crop_height = int(height * 0.2)

    # Crop the top 20%
    cropped_img = img[crop_height:, :]

    # Save the cropped image
    cv2.imwrite(output_path, cropped_img)

    return output_path

# Function to clean the image using OpenCV
def clean_image(image_path, output_path):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, binary_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # Remove noise using a median blur
    denoised_image = cv2.medianBlur(binary_image, 3)

    # Save the cleaned image
    cv2.imwrite(output_path, denoised_image)

    return output_path

# Function to preprocess the image for OCR
def preprocess_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert to grayscale
    gray_image = image.convert("L")

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)

    # Apply thresholding
    threshold_image = enhanced_image.point(lambda x: 0 if x < 128 else 255)

    return threshold_image

# Function to extract numbers using Tesseract OCR
def extract_numbers(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(preprocessed_image, config="--psm 6")

    # Use a regular expression to extract numbers
    numbers = re.findall(r'\d+', text)

    return numbers

# Main process
def main():
    option1 = "257 1630"
    option2 = "757 1630"
    option3 = "257 1888"
    option4 = "757 1888"
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

    # Print results
    print("Extracted Numbers:", numbers)

# Run the main process
if __name__ == "__main__":
    main()
