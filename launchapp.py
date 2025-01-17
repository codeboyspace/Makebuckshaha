import subprocess
import time
import xml.etree.ElementTree as ET

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
                time.sleep(30)
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

def wait_for_app_to_load(max_wait=1):
    """
    Waits for the app to load, up to a maximum number of seconds.
    """
    print(f"Waiting for the app to load (up to {max_wait} seconds)...")
    time.sleep(max_wait)

def main_loop():
    while True:
        # Wait for app to load
        wait_for_app_to_load(1)

        # Tap "Earn Now" at the top center of the screen
        print("Tapping on center of the screen...")
        tap_on_center()
        time.sleep(1)

        # Tap "Claim Now!"
        print("Looking for 'Earn Now'...")
        find_and_tap_button_by_description("jackpot")
        time.sleep(1)

        # Tap "Claim Now!"
        print("Looking for 'Claim Now!'...")
        find_and_tap_button_with_texts(["Claim Now!"], "Claim Now!")
        time.sleep(1)

        print("Looking for Watch Ad...")
        find_and_tap_button_by_description(["Watch Ad"],"Watch Ad")

        # Check if "Verify" is available
        print("Looking for 'Verify'...")
        if find_and_tap_button_with_texts(["Verify"], "Verify"):
            print("Found and tapped 'Verify'. Waiting for further options...")

        # Wait for "Continue" or "Retry" to appear
        print("Waiting for 'Continue' or 'Retry' to appear...")
        while not find_and_tap_button_with_texts(["Continue", "Retry"], "Continue or Retry"):
            time.sleep(1)
            print("Looking for 'Tickets'...")
            find_and_tap_button_by_description("Tickets")
            time.sleep(1)
            find_and_tap_button_by_description("Play a game")
        print("Tapped 'Continue' or 'Retry'.")

        

# Start the main loop
main_loop()
