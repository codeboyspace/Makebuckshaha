import os
import subprocess
import time
import xml.etree.ElementTree as ET

def find_and_tap_button_with_text(text):
    # Dump the current UI hierarchy
    subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True)
    tapped = False
    # Pull the dumped XML file to the local machine
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml"], check=True)
    
    # Parse the XML file
    tree = ET.parse("window_dump.xml")
    root = tree.getroot()
    
    # Find the node with the specified text
    for node in root.iter("node"):
        if node.attrib.get("content-desc") == text:
            # Extract bounds
            bounds = node.attrib.get("bounds")
            if bounds:
                # Extract coordinates from bounds
                bounds = bounds.strip("[]").split("][")
                left_top = list(map(int, bounds[0].split(",")))
                right_bottom = list(map(int, bounds[1].split(",")))
                
                # Calculate the center point
                x = (left_top[0] + right_bottom[0]) // 2
                y = (left_top[1] + right_bottom[1]) // 2
                
                # Simulate the tap
                subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
                print(f"Tapped on the button with text: {text}")
                
                return
    print(f"No button found with text: {text}")
def tap_on_center():
    screen_size = os.popen('adb shell wm size').read()
    # Extract width and height
    width, height = map(int, screen_size.split(":")[1].strip().split("x"))

    # Calculate center coordinates
    center_x = width // 2
    center_y = height // 2

    # Tap the center
    os.system(f"adb shell input tap {center_x} {center_y}")

find_and_tap_button_with_text("Complete")
time.sleep(1)
find_and_tap_button_with_text("Claim Now!")
time.sleep(1)
find_and_tap_button_with_text("Watch Ad")

tap_on_center()

