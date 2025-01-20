import os
import subprocess
import cv2 
from PIL import Image, ImageEnhance
import pytesseract
import xml.etree.ElementTree as ET
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

#Close Special Ad's
def find_and_tap_button_by_description(description):
    """
    Finds a button by its content description and taps on it.

    :param description: The content description of the button to tap.
    """
    # Generate the UI dump and pull the XML file
    subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True)
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml"], check=True)

    # Parse the XML file
    tree = ET.parse("window_dump.xml")
    root = tree.getroot()

    # Loop through the XML to find the button with the matching content-desc
    for node in root.iter("node"):
        content_desc = node.attrib.get("content-desc")
        resource_desc = node.attrib.get("resource-id")
        if content_desc and description in content_desc:
            bounds = node.attrib.get("bounds")
            if bounds:
                # Parse the bounds to extract the coordinates
                bounds = bounds.strip("[]").split("][")
                left_top = list(map(int, bounds[0].split(",")))
                right_bottom = list(map(int, bounds[1].split(",")))

                # Calculate the center coordinates
                x = (left_top[0] + right_bottom[0]) // 2
                y = (left_top[1] + right_bottom[1]) // 2

                # Tap on the calculated coordinates
                subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
                print(f"Tapped on the button with content-desc: '{description}' at coordinates: ({x}, {y})")
                return True
            
        if resource_desc and description in resource_desc:
            bounds = node.attrib.get("bounds")
            if bounds:
                # Parse the bounds to extract the coordinates
                bounds = bounds.strip("[]").split("][")
                left_top = list(map(int, bounds[0].split(",")))
                right_bottom = list(map(int, bounds[1].split(",")))

                # Calculate the center coordinates
                x = (left_top[0] + right_bottom[0]) // 2
                y = (left_top[1] + right_bottom[1]) // 2

                # Tap on the calculated coordinates
                subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
                print(f"Tapped on the button with content-desc: '{description}' at coordinates: ({x}, {y})")
                return True

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

# Function to check for "Claim"
def check_for_claim(text):
    return "Claim" in text

# Function to parse XML and find bounds of a button by keyword in resource-id
def find_bounds_by_keyword(xml_content, keyword):
    match = re.search(rf'<node.*?resource-id="[^"]*{keyword}[^"]*".*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml_content)
    if match:
        x_center = (int(match.group(1)) + int(match.group(3))) // 2
        y_center = (int(match.group(2)) + int(match.group(4))) // 2
        return x_center, y_center
    return None

def checkBackButton(xml_content, keyword):
    match = re.search(rf'<node.*?content-desc="[^"]*{keyword}[^"]*".*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml_content)
    if match:
        x_center = (int(match.group(1)) + int(match.group(3))) // 2
        y_center = (int(match.group(2)) + int(match.group(4))) // 2
        return x_center, y_center
    return None

# Function to check for navigation bar presence
def is_navigation_bar_present():
    os.system("adb shell uiautomator dump /sdcard/window_dump.xml > result.txt")
    with open("result.txt",'r') as log:
        status = log.readline()
        print(status)
        if(status.find("")):
            print("Failed from skip/close")
            os.system("adb shell input tap 1002 100")
            os.system("adb shell input tap 1002 120")
            return True
        else:
            print("Success")


    os.system("adb pull /sdcard/window_dump.xml window_dump.xml")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        content = file.read()
    # Check if "android:id/navigationBarBackground" is in the content
    if "android:id/navigationBarBackground" in content:
        return True
    return False

# Function to handle skip or close and close alert with "Continue"
def handle_skip_or_close():
    os.system("adb shell uiautomator dump /sdcard/window_dump.xml")
    os.system("adb shell uiautomator dump /sdcard/window_dump.xml > result.txt")
    with open("result.txt",'r') as log:
        status = log.readline()
        print(status)
        if(status.find("")):
            print("Failed from skip/close")
            os.system("adb shell input tap 1002 100")
            os.system("adb shell input tap 1002 120")
            return True
        else:
            print("Success")

    os.system("adb pull /sdcard/window_dump.xml window_dump.xml")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        content = file.read()

    # Check for the presence of a "close" button or "skip" button
    close_bounds = find_bounds_by_keyword(content, "close")
    close_ad = find_bounds_by_keyword(content, "Close Ad")
    close_ad_desc = find_and_tap_button_by_description("Close Ad")
    skip_bounds = find_bounds_by_keyword(content, "skip")

    # If "close" is found, tap on "close"
    if close_bounds:
        x, y = close_bounds
        os.system(f"adb shell input tap {x} {y}")
        print(f"Tapped on button with resource-id containing 'close' at ({x}, {y})")
        return True
    
    elif close_ad:
        x, y = close_ad
        os.system(f"adb shell input tap {x} {y}")
        print(f"Tapped on button with resource-id containing 'close ad' at ({x}, {y})")
        return True
    
    elif close_ad_desc:
        x, y = close_ad_desc
        os.system(f"adb shell input tap {x} {y}")
        print(f"Tapped on button with resource-id containing 'close ad' at ({x}, {y})")
        return True
    
    elif skip_bounds:
        x, y = skip_bounds
        os.system(f"adb shell input tap {x} {y}")
        print(f"Tapped on button with resource-id containing 'skip' at ({x}, {y})")
        
        return True
    return False

# Function to handle the alert and tap "Continue"
def handle_alert_continue():
    # Checking logs for the specific error message
    os.system("adb logcat -d | grep 'ERROR: could not get idle state'")
    error_logs = os.popen("adb logcat -d | grep 'ERROR: could not get idle state'").read()
    
    # If the error "ERROR: could not get idle state" is found in the logs, close the alert
    if "ERROR: could not get idle state" in error_logs:
        # Tap the "Continue" button on the alert
        os.system("adb shell input tap 717 1300")  # Coordinates for "Continue" button (this may need adjusting)
        print("Tapped 'Continue' to handle alert.")
        
        # Wait for 16 seconds to allow the alert to be closed
        time.sleep(16)

        # Check again for the "close" button after the alert is closed
        print("Attempting to close after waiting 16 seconds.")
        os.system("adb shell input tap 717 1300")  # Tap "Continue" again to handle the alert if it's still open.
        time.sleep(16)
        return True
    return False

def navibar():
    os.system("adb pull /sdcard/window_dump.xml window_dump.xml")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        content = file.read()
    # Check if "android:id/navigationBarBackground" is in the content
        backkey = checkBackButton(content, "Back")
        if backkey != None:
            return True
        else:
            return False

# Main process
def main():
    original_image = "screen.png"
    cropped_image = "cropped_image.png"
    cleaned_image = "cleaned_image.png"
    clicks = 0
    while True:
        RunAPP = navibar()
        print(RunAPP)
        # Step 1: Check for navigation bar presence
        if not is_navigation_bar_present():
            print("Navigation bar not found. Checking for skip or close buttons...")
            while not handle_skip_or_close():
                pass  # Keep checking until a skip or close button is found and handled
            continue

        if RunAPP:
        # Step 2: Capture a screenshot and save it
            os.system(f"adb exec-out screencap -p > {original_image}")
            print("Screenshot saved as 'screen.png'")

            # Step 3: Crop and clean the image
            cropped_image = crop_image(original_image, cropped_image)
            cleaned_image = clean_image(cropped_image, cleaned_image)

            # Step 4: Extract numbers and text
            numbers, text = extract_numbers(cleaned_image)
            print(f"Numbers:{numbers},Text: {text}")

            # Step 5: Check for "Claim" in the text
            if check_for_claim(text):
                clicks += 1
                os.system("adb shell input tap 757 1950")
                print(f"Tapped 'Claim': {clicks}")
                if clicks > 25:
                    return

                # After tapping "Claim", check for skip or close button again
                print("Claim tapped, checking for skip or close button again...")
                while not handle_skip_or_close():
                    pass  # Keep checking until a skip or close button is found and handled

                continue

            # Step 6: Process question and options
            if len(numbers) >= 4 and len(numbers)<=5:
                question = "".join(numbers[:-4])
                options = numbers[-4:]
                coordinates = {0: "257 1630", 1: "757 1630", 2: "257 1888", 3: "757 1888"}

                for i, option in enumerate(options):
                    if question in option or sum(1 for digit in question if digit in option) >= 3:
                        adb_command = f"adb shell input tap {coordinates[i]}"
                        os.system(adb_command)
                        print(f"Question: {question}, Options: {options}, Tapped: {adb_command}")
                        break
            else:
                print("Not enough numbers to process question and options.")
                print("Claim tapped, checking for skip or close button again...")
                while not handle_skip_or_close():
                    pass  # Keep checking until a skip or close button is found and handled
        else:
            print("Not enough numbers to process question and options.")
            print("Claim tapped, checking for skip or close button again...")
            while not handle_skip_or_close():
                pass  # Keep checking until a skip or close button is found and handled

if __name__ == "__main__":
    main()
