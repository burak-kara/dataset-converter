import glob
import os
import math as m
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R

SS = "\\"
ROOT_FOLDER = "results\\uid-*"
INNER_FOLDER = "\\test0\\"
HEADS = "heads"
VIDEOS = ["Diving-2OzlksZBTiA\\*", "Paris-sJxiPiAaB4k\\*", "Rhino-training-7IWp875pCxQ\\*",
		  "Rollercoaster-8lsB-P8nGSM\\*", "Timelapse-CIw8R8thnm8\\*", "Venise-s-AJRFQuAtE\\*"]

folders = glob.glob(ROOT_FOLDER)

try:
	os.makedirs(HEADS)
except:
	print("heads folder is exist. Dont forget to create a backup")
	sys.exit(0)


class Quaternion:
	def __init__(self, line):
		self.q = [line[2], line[3], line[4], line[1]]
		self.x = line[2]
		self.y = line[3]
		self.z = line[4]
		self.w = line[1]

	def to_rotation(self):
		return R.from_quat(self.q)

	def to_euler(self):
		angles = self.to_rotation().as_euler("ZYX", degrees=True)
		return [round(elem, 2) for elem in angles]


def get_quaternion_from_euler(roll, pitch, yaw):
	# https://automaticaddison.com/how-to-convert-euler-angles-to-quaternions-using-python/
	qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
	qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
	qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
	qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

	return [qx, qy, qz, qw]


# for each user folder
for i in range(len(folders)):
	user_folder_path = folders[i]
	user_folder = user_folder_path.split(SS)[-1]

	# for each video folder inside a user folder
	for v_i in range(len(VIDEOS)):
		video = VIDEOS[v_i]  # Set video
		video_name = video.split('-')[0]
		path = user_folder_path + INNER_FOLDER + video
		log_file = glob.glob(path)
		print(log_file)
		if log_file:
			with open(log_file[0]) as file:
				with open(HEADS + SS + video_name.lower() + "_" + str(i), "w") as extracted:
					lines = file.readlines()
					for line in lines:
						line = line.replace('\n', '').split()
						pts = int(float(line[0]) * 1000)  # convert timestamp from seconds to milliseconds
						del line[1]  # clear frame id
						euler = Quaternion(line).to_euler()
						modified_line = ' '.join([str(elem) for elem in [pts] + euler]) + "\n"
						extracted.write(modified_line)
					# sys.exit(1)
