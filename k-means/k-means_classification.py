from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import cv2, os

def inputNumber(message):
	while True:
		try:
			userInput = int(input(message))
		except ValueError:
			print("Not an integer! Please type an int.")
			continue
		else:
			return userInput
			break


while True:
	img_name = input('Name (leave it empty to exit): ')
	if not img_name:
		raise SystemExit
	elif not os.path.isfile(img_name):
		print('File name doesn\'t exist or has no extention, please try again.\n')
	else:
		k = inputNumber('How many masks: ')
		b = inputNumber('Blur strength: ')
		print('\nWorking...')

		# create folder
		dateTimeObj = datetime.now()
		timestampStr = dateTimeObj.strftime('%y%m%d%H%M%S')
		path = timestampStr
		os.makedirs(path)
		
		# read
		img = cv2.imread(img_name)
		image_2d = img.reshape((img.shape[0] * img.shape[1], 3))

		# supplying the number of clusters we wish to generate
		# kmeans_cluster = KMeans(n_clusters=k) # this is slower but more accurate
		kmeans_cluster = MiniBatchKMeans(n_clusters=k) 
		kmeans_cluster.fit(image_2d) # clusters our list of pixels

		cluster_centers = kmeans_cluster.cluster_centers_ # dominant colors array
		cluster_labels = kmeans_cluster.labels_

		result = cluster_centers[cluster_labels]
		result = np.reshape(result, (img.shape))
		cv2.imwrite(f'{path}/colormap.png', result)

		# create masks and classification map
		indexed = img.copy()
		for i in range(k):
			sample = cluster_centers[i]

			mask = cv2.inRange(result, sample, sample)

			if b != 0:
				if not b % 2 != 0:
					b += 1
				mask = cv2.GaussianBlur(mask, (b, b), 0)

			cv2.imwrite(f'{path}/mask{i}.png', mask)

			indexed[mask>0] = (i, i, i)

		cv2.imwrite(f'{path}/index_map.png', indexed)

		print('\nDone.\n')

