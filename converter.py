import glob
import os
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R

SS = "\\"
NEW_LINE = "\n"
ROOT_FOLDER = "results\\uid-*"
INNER_FOLDER = "\\test0\\"
HEADS = "heads"
VIDEOS = ["Diving-2OzlksZBTiA\\*", "Paris-sJxiPiAaB4k\\*", "Rhino-training-7IWp875pCxQ\\*",
		  "Rollercoaster-8lsB-P8nGSM\\*", "Timelapse-CIw8R8thnm8\\*", "Venise-s-AJRFQuAtE\\*"]
FOLDERS = []


# helper math functions
def sin(xx):
	return np.sin(xx / 2)


def cos(xx):
	return np.cos(xx / 2)


# seconds to ms
def as_ms(sec):
	return int(float(sec) * 1000)


class Quaternion:
	def __init__(self, line):
		self.q = [line[2], line[3], line[4], line[1]]

	def to_rotation(self):
		return R.from_quat(self.q)

	def to_euler(self):
		angles = self.to_rotation().as_euler("ZYX", degrees=True)
		return [round(elem, 2) for elem in angles]

	@staticmethod
	def create_from_euler(euler_form):
		# https://automaticaddison.com/how-to-convert-euler-angles-to-quaternions-using-python/
		roll, pitch, yaw = euler_form
		qx = sin(roll) * cos(pitch) * cos(yaw) - cos(roll) * sin(pitch) * sin(yaw)
		qy = cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * cos(pitch) * sin(yaw)
		qz = cos(roll) * cos(pitch) * sin(yaw) - sin(roll) * sin(pitch) * cos(yaw)
		qw = cos(roll) * cos(pitch) * cos(yaw) + sin(roll) * sin(pitch) * sin(yaw)

		return Quaternion([qw, qx, qy, qz])


def write_output(video_name, folder_i, file):
	with open(HEADS + SS + video_name.lower() + "_" + str(folder_i), "w") as extracted:
		lines = file.readlines()
		for line in lines:
			line = line.replace(NEW_LINE, '').split()
			# convert timestamp from seconds to milliseconds
			pts = as_ms(line[0])
			# clear frame id
			del line[1]
			euler = Quaternion(line).to_euler()
			modified_line = ' '.join([str(elem) for elem in [pts] + euler]) + NEW_LINE
			extracted.write(modified_line)


def open_log_file(log_file, video_name, f_i):
	# Some users did not test all videos
	if log_file:
		with open(log_file[0]) as file:
			write_output(video_name, f_i, file)


def process():
	# for each user folder
	for f_i in range(len(FOLDERS)):
		user_folder_path = FOLDERS[f_i]

		# for each video folder inside a user folder
		for v_i in range(len(VIDEOS)):
			video = VIDEOS[v_i]
			video_name = video.split('-')[0]
			log_file = get_folders(user_folder_path + INNER_FOLDER + video)
			open_log_file(log_file, video_name, f_i)


def get_folders(path):
	return glob.glob(path)


def init():
	global FOLDERS
	FOLDERS = get_folders(ROOT_FOLDER)

	try:
		os.makedirs(HEADS)
	except:
		print("heads folder is exist. Dont forget to create a backup")
		sys.exit(0)


if __name__ == '__main__':
	init()
	process()
