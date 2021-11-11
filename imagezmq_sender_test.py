import jetson.utils
import jetson.inference

import socket
import imagezmq

import argparse
import sys
import time

def current_milli_time():
    return round(time.time() * 1000)

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="csi://0", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)



sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)

rpi_name = socket.gethostname()

print(rpi_name)

print('hi')

while True:
	img = input.Capture()
	timestamp = current_milli_time()

	cv_img = jetson.utils.cudaAllocMapped(width=img.width, height=img.height, format="bgr8")

	jetson.utils.cudaConvertColor(img, cv_img)

	jetson.utils.cudaDeviceSynchronize()

	cv_npimg = jetson.utils.cudaToNumpy(cv_img)
	print('sending image at ', timestamp)
	sender.send_image(timestamp, cv_npimg)
	time.sleep(0.5)
	# time.sleep(2.0)


