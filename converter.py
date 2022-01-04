import glob
import os
import math as m
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

def q_conjugate(q):
	w, x, y, z = q
	return w, -x, -y, -z


def qv_mult(q1, v1):
	q2 = (0.0,) + v1
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]


def q_mult(q1, q2):
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2
	w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
	x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
	y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
	z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
	return w, x, y, z


def quaternion_to_euler(w, x, y, z):
	t0 = 2 * (w * x + y * z)
	t1 = 1 - 2 * (x * x + y * y)
	X = m.atan2(t0, t1)

	t2 = 2 * (w * y - z * x)
	t2 = 1 if t2 > 1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = m.asin(t2)

	t3 = 2 * (w * z + x * y)
	t4 = 1 - 2 * (y * y + z * z)
	Z = m.atan2(t3, t4)

	return X * 180 / m.pi, Y * 90 / m.pi, Z * 180 / m.pi


def quaternion_to_euler2(w, x, y, z):
	yaw = m.atan2(2.0 * (y * z + w * x), w * w - x * x - y * y + z * z)
	pitch = m.asin(-2.0 * (x * z - w * y))
	roll = m.atan2(2.0 * (x * y + w * z), w * w + x * x - y * y - z * z)

	return yaw * 180 / m.pi, pitch * 90 / m.pi, roll * 180 / m.pi


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
						line[0] = int(float(line[0]) * 1000)  # convert timestamp from seconds to milliseconds
						del line[1]  # clear frame id
						print(quaternion_to_euler(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
						# line[1:] = quaternion_to_euler2(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
						print(quaternion_to_euler2(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
					# extracted.write(modified_line)
					sys.exit(1)
