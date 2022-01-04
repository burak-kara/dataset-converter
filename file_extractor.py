import glob
import os
import sys

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
# sys.exit(0)

# for each user folder
for i in range(len(folders)):
	folder = folders[i]
	uid = folder.split('\\')[-1][4:]

	# for each video folder inside a user folder
	for v_i in range(len(VIDEOS)):
		video = VIDEOS[v_i]  # Set video
		video_name = video.split('-')[0]
		path = folder + INNER_FOLDER + video
		log_file = glob.glob(path)
		if log_file:
			with open(log_file[0]) as file:
				with open(HEADS + "\\head_" + video_name.lower() + "_" + str(i), "w") as extracted:
					lines = file.readlines()
					for line in lines:
						line = line.replace('\n', '').split()
						del line[1:3]  # clear unnecessary data
						ts = int(float(line[0]) * 1000)
						zz = 0
						yy = float(line[2]) * 90
						xx = float(line[3]) * 180
						modified_line = ' '.join(map(str, [ts, xx, yy, zz, '\n']))
						extracted.write(modified_line)
