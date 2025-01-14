import os

# Get the full path of the batch file
batch_file = os.path.join(os.getcwd(), "closeopentest.py")

# Use os.startfile to open the batch file as if double-clicked
os.startfile(batch_file)
