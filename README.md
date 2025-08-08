

SECURITYCAMERA_OPENCWPYWHAT
Transforming Security with Intelligent, Real-Time Surveillance
This open-source project transforms a standard webcam into an intelligent security system. It integrates real-time computer vision using OpenCV and YOLOv3 to detect specific objects and sends instant security alerts via WhatsApp, complete with a snapshot and location data.

Overview
securitycamera_opencwpywhat is a tool that empowers developers to build smarter security systems with ease. It streamlines the process of monitoring a live video feed, identifying objects of interest, and triggering automated responses. This makes it an ideal solution for creating custom, intelligent surveillance setups for home or business use.

Core Features
🎯 Real-Time Detection: Monitors live webcam feeds to identify over 80 different objects instantly using the powerful YOLOv3 model.

🚨 Automated WhatsApp Alerts: Captures a snapshot the moment a target object is detected and sends it directly to your phone via WhatsApp.

📍 Location Tracking: Fetches the approximate geographical location using the device's IP address and includes a Google Maps link in the alert.

⚙️ Easy Configuration: Simple, readable Python script allows you to easily define the target object, recipient phone number, and detection sensitivity.

⏱️ Spam Prevention: Includes a configurable cooldown period to prevent multiple alerts for the same event.

🧱 Modular Architecture: The code is organized into clear functions, making it easy to understand, modify, and scale.

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

Prerequisites
This project requires the following to be installed on your system:

Programming Language: Python 3.8 or newer

Package Manager: pip

YOLOv3 Model Files: You need the weights, config, and names files for the model to work.

yolov3.weights

yolov3.cfg

coco.names
You can download these from the official YOLO website or by using the command line:

Bash

wget https://pjreddie.com/media/files/yolov3.weights
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
WhatsApp Web: You must be logged into WhatsApp Web on your default browser for the notifications to work.

Installation
Build securitycamera_opencwpywhat from the source and install dependencies:

Clone the repository:

Bash

git clone https://github.com/DarKAlKI-gt/securitycamera_opencwpywhat
Navigate to the project directory:

Bash

cd securitycamera_opencwpywhat
Create a requirements.txt file with the following content:

Plaintext

opencv-python
numpy
pywhatkit
requests
Install the dependencies:

Bash

pip install -r requirements.txt
Configuration
Before running the script, you need to configure a few parameters inside the main Python file (e.g., main.py):

TARGET_OBJECT: Set the string of the object you want to detect (e.g., "person", "car", "cell phone").

PHONE_NUMBER: Set the recipient's phone number as a string, including the country code (e.g., "+91xxxxxxxxxx").

CONFIDENCE_THRESHOLD: Adjust the model's sensitivity (e.g., 0.5 for 50%).

SEND_COOLDOWN: Set the wait time in seconds between alerts (e.g., 60).

Usage
Ensure all prerequisites and configuration steps are complete. Run the project with:

Bash

python main.py
The script will initialize the webcam, and a window titled "Security Feed" will appear. Press the 'q' key on your keyboard to stop the program.

Testing
Currently, the project does not have a formal test framework. You can test the full functionality by:

Running the main.py script.

Placing the TARGET_OBJECT in front of the webcam.

Verifying that a bounding box appears around the object in the "Security Feed" window.

Confirming that you receive a WhatsApp message with the snapshot and location link.
