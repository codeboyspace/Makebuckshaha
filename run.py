import os
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import pyautogui
import subprocess
import re
import time

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
    print(numbers)
    return numbers, text  # Return both numbers and the full text

# Function to check if the text contains "Claim"
def check_for_claim(text):
    if "Claim" in text:
        return True
    return False

def restart_app():
    print("Restarting the app...")
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(1)
    os.system("adb shell input swipe 500 1000 300 10")
    time.sleep(1)
    os.system("adb shell input swipe 500 1000 300 10")
    time.sleep(1)
    os.system("adb shell input keyevent 4")
    time.sleep(2)
    time.sleep(9)
    os.system("adb shell input tap 757 1130")
    os.system("adb shell input tap 757 1799")
    #time.sleep(2)
    #os.system("adb shell input tap 295 2150")
    print("App restarted and inputs executed.")

# Function to determine the question and options and execute ADB command
def process_and_click(numbers):
    if len(numbers) < 4:
        print(numbers)
        print("Not enough numbers extracted to form a question and options.")
        restart_app()
        return

    # Form the question by joining all numbers except the last 4
    question = "".join(numbers[:-4])

    # Extract the last 4 numbers as options
    options = numbers[-4:]

    # Coordinates for each option
    coordinates = {
        0: "257 1630",
        1: "757 1630",
        2: "257 1888",
        3: "757 1888"
    }

    # Improved logic to check if the answer (question number) is already in the options
    def is_question_in_option(question, option):
        return question in option

    # First, check if any option exactly matches the question number
    for i, option in enumerate(options):
        if is_question_in_option(question, option):
            coords = coordinates[i]
            adb_command = f"adb shell input tap {coords}"
            os.system(adb_command)
            print(f"Question: {question}")
            print(f"Options: {options}")
            print(f"Exact match found with option at index {i}. Executed command: {adb_command}")
            return

    # If no exact match, proceed to check for 3 or 2 digit match
    def is_match(question, option):
        match_count = sum(1 for digit in question if digit in option)
        return match_count >= 3  # At least 3 matching digits

    for i, option in enumerate(options):
        if is_match(question, option):
            coords = coordinates[i]
            adb_command = f"adb shell input tap {coords}"
            os.system(adb_command)
            print(f"Question: {question}")
            print(f"Options: {options}")
            print(f"Correct option found at index {i}. Executed command: {adb_command}")
            return

    print("No suitable match found for the question in options.")
    adb_command = "adb shell input tap 757 1630"
    os.system(adb_command)

# Main process
def main():
    # Paths
    clicks=0
    original_image = "screen.png"
    cropped_image = "cropped_image.png"
    cleaned_image = "cleaned_image.png"

    while True:
        # Capture a screenshot and save it
        os.system(f"adb exec-out screencap -p > {original_image}")
        print("Screenshot saved as 'screen.png'")

        # Step 1: Crop the top 20% of the image
        cropped_image = crop_image(original_image, cropped_image)

        # Step 2: Clean the image
        cleaned_image = clean_image(cropped_image, cleaned_image)

        # Step 3: Extract numbers and full text from the cleaned image
        numbers, text = extract_numbers(cleaned_image)

        # Step 4: Check if "Claim" is in the extracted text
        if check_for_claim(text):
            clicks+=1
            adb_command = "adb shell input tap 757 1950"
            os.system(adb_command)
            print(f"Tapped Claim:{clicks}")
            time.sleep(33)
            back_button = "adb shell input keyevent 4"
            os.system(back_button)
              # Exit the loop after clicking on "Claim"

        # Step 5: Process numbers and execute tap command for question options
        process_and_click(numbers)

        # Sleep before taking the next screenshot (you can adjust the sleep time as needed)
        time.sleep(1)

if __name__ == "__main__":
    main()

