import os , subprocess , time
clicks = 0
while True:
    os.system("adb shell input tap 257 1630")
    time.sleep(0.5)
    os.system("adb shell input tap 757 1630")
    time.sleep(0.5)
    os.system("adb shell input tap 257 1888")
    time.sleep(0.5)
    os.system("adb shell input tap 757 1888")
    time.sleep(0.5)
    adb_command = "adb shell input tap 757 1950"
    os.system(adb_command)
    clicks+=1

    print(f"Tapped Claim: {clicks}")
