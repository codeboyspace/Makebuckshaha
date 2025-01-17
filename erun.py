import os
import subprocess
import time
import xml.etree.ElementTree as ET

def find_and_tap_button_with_texts(texts):
    """
    Finds and taps a button with any of the specified texts.

    :param texts: A list of possible texts for the button.
    :return: True if a button was found and tapped, otherwise False.
    """
    # Dump the current UI hierarchy
    subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True)
    # Pull the dumped XML file to the local machine
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml"], check=True)
    
    # Parse the XML file
    tree = ET.parse("window_dump.xml")
    root = tree.getroot()
    
    # Find the node with any of the specified texts
    for node in root.iter("node"):
        for text in texts:
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
                    return True
    return False

def tap_on_center():
    screen_size = os.popen('adb shell wm size').read()
    # Extract width and height
    width, height = map(int, screen_size.split(":")[1].strip().split("x"))

    # Calculate center coordinates
    center_x = width // 2
    center_y = height // 2

    # Tap the center
    os.system(f"adb shell input tap {center_x} {center_y}")

def wait_for_buttons_and_tap(possible_texts, max_wait=300, check_interval=5):
    """
    Waits for a button with any of the specified texts to appear and taps it once found.

    :param possible_texts: A list of possible texts for the button.
    :param max_wait: Maximum time to wait in seconds (default 300 seconds).
    :param check_interval: Time interval between checks in seconds (default 5 seconds).
    :return: True if a button was found and tapped, otherwise False.
    """
    waited = 0
    while waited < max_wait:
        print(f"Checking for buttons with texts: {possible_texts}...")
        if find_and_tap_button_with_texts(possible_texts):
            print(f"Button found and tapped.")
            return True
        pause(check_interval)
        waited += check_interval
    print(f"Buttons '{possible_texts}' not found within {max_wait} seconds.")
    return False
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
                pause(30)
                return True
            
def tap_on_center():
    """
    Taps the center of the screen.
    """
    screen_size = subprocess.check_output("adb shell wm size", shell=True).decode()
    width, height = map(int, screen_size.split(":")[1].strip().split("x"))

    center_x = width // 2
    center_y = height // 2

    subprocess.run(["adb", "shell", "input", "tap", str(center_x), str(center_y)])
    print("Tapped on the center of the screen.")

def wait_for_app_to_load(max_wait=10):
    """
    Waits for the app to load, up to a maximum number of seconds.
    """
    print(f"Waiting for the app to load (up to {max_wait} seconds)...")
    pause(max_wait)
def find_and_tap_button_with_texts2(texts, description=""):
    """
    Finds and taps a button with any of the specified texts.

    :param texts: A list of possible texts for the button.
    :param description: A description of what the button is for logging purposes.
    :return: True if a button was found and tapped, otherwise False.
    """
    subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True)
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml"], check=True)

    tree = ET.parse("window_dump.xml")
    root = tree.getroot()

    for node in root.iter("node"):
        for text in texts:
            if node.attrib.get("content-desc") == text:
                bounds = node.attrib.get("bounds")
                if bounds:
                    bounds = bounds.strip("[]").split("][")
                    left_top = list(map(int, bounds[0].split(",")))
                    right_bottom = list(map(int, bounds[1].split(",")))

                    x = (left_top[0] + right_bottom[0]) // 2
                    y = (left_top[1] + right_bottom[1]) // 2

                    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
                    print(f"Tapped on the button with text '{text}' for '{description}'.")
                    return True
                
def appopen():
        wait_for_app_to_load(10)

        # Tap "Earn Now" at the top center of the screen
        print("Tapping on center of the screen...")
        tap_on_center()
        pause(1)

        # Tap "Claim Now!"
        print("Looking for 'Earn Now'...")
        find_and_tap_button_by_description("jackpot")
        pause(1)

        # Tap "Claim Now!"
        print("Looking for 'Claim Now!'...")
        find_and_tap_button_with_texts(["Claim Now!"], "Claim Now!")
        pause(1)

        print("Looking for Watch Ad...")
        find_and_tap_button_by_description(["Watch Ad"],"Watch Ad")

        # Check if "Verify" is available
        print("Looking for 'Verify'...")
        if find_and_tap_button_with_texts(["Verify"], "Verify"):
            print("Found and tapped 'Verify'. Waiting for further options...")

        # Wait for "Continue" or "Retry" to appear
        print("Waiting for 'Continue' or 'Retry' to appear...")
        while not find_and_tap_button_with_texts2(["Continue", "Retry"], "Continue or Retry"):
            pause(1)
            print("Looking for 'Tickets'...")
            find_and_tap_button_by_description("Tickets")
            pause(1)
            find_and_tap_button_by_description("Play a game")
        print("Tapped 'Continue' or 'Retry'.")

def pause(seconds):
    pause(seconds)

def main_loop():
    while True:
        find_and_tap_button_with_texts(["Complete"])
        pause(1)
        find_and_tap_button_with_texts(["Claim"])
        pause(1)
        find_and_tap_button_with_texts(["Claim Now!"])
        pause(1)
        find_and_tap_button_with_texts(["Watch Ad"])
        while not find_and_tap_button_with_texts2(["Continue", "Retry"], "Continue or Retry"):
            pause(1)
            print("Looking for 'Tickets'...")
            find_and_tap_button_by_description("Tickets")
            pause(1)
            if find_and_tap_button_with_texts(["Watch Ad"]) == True:
                pause(5)
            find_and_tap_button_by_description("Play a game")
        find_and_tap_button_with_texts(["Verify"])
        tap_on_center()
        find_and_tap_button_with_texts(["Install"])
        
        # Wait for "Open" or "Play" button after tapping "Install"
        print("Waiting for the 'Open' or 'Play' button to appear...")
        if wait_for_buttons_and_tap(["Open", "Play"]):
            # Wait for 2.5 minutes after tapping "Open" or "Play"
            print("Waiting for 2.5 minutes before relaunching the app...")
            pause(150)
            
            # Relaunch the app
            print("Launching the app: com.rayolesoftware.cash.daddy")
            subprocess.run(["adb", "shell", "am", "start", "-n", 
                            "com.rayolesoftware.cash.daddy/.MainActivity"], check=True)
            appopen(10)

# Start the main loop
main_loop()
