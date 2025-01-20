import os
import subprocess
import xml.etree.ElementTree as ET


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
        content_desc = node.attrib.get("content_desc")
        resource_desc = node.attrib.get("resource-id")
        print(resource_desc)
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


find_and_tap_button_by_description("close")
find_and_tap_button_by_description("task_view_single")