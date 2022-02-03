import glob
import os
import sys

SS = "\\"
NEW_LINE = "\n"
SRC_FOLDER = "RawData"
RESULTS_HEAD = "heads"
RESULTS_GAZE = "gaze"
TASKS = 4 + 1  # The actual count is 4 but for boundary reasons added +1
VIDEOS = 15 + 1
USERS = 30 + 1
FOLDERS = []


def write_gaze_file(file_name):
	pass


def write_head_file(file_name):
	pass


def open_data_file(file_path):
	with open(file_path) as f:
		write_head_file(file_path)
		write_gaze_file(file_path)
		lines = f.readlines()
		for line in lines:
			print(line)
			break


def create_file_name(user, video, task):
	return "User_" + f"{user:02d}" + "_Video_" + f"{video:02d}" + "_Task_" + str(task) + ".txt"


def process():
	user = 0
	while user < USERS:
		for video in range(1, VIDEOS):
			if video % 3 == 1:
				user += 1
				if user == USERS:
					break
			for task in range(1, TASKS):
				file = create_file_name(user, video, task)
				open_data_file(SRC_FOLDER + SS + file)


def get_folders(path):
	return glob.glob(path)


def init():
	try:
		# os.makedirs(RESULTS_HEAD)
		# os.makedirs(RESULTS_GAZE)
		print("")
	except:
		print("heads folder is exist. Dont forget to create a backup")
		sys.exit(0)


if __name__ == '__main__':
	init()
	process()
