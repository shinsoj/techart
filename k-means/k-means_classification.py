import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import cv2

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


k = inputNumber('How much masks do you want?: ')
b = inputNumber('Blur strength: ')
print('Working...')

# read
img = cv2.imread('input.png')

image_2d = img.reshape((img.shape[0] * img.shape[1], 3))

# supplying the number of clusters we wish to generate
# kmeans_cluster = KMeans(n_clusters=k) # this is slower but more accurate
kmeans_cluster = MiniBatchKMeans(n_clusters=k) 
kmeans_cluster.fit(image_2d) # clusters our list of pixels

cluster_centers = kmeans_cluster.cluster_centers_ # dominant colors array
cluster_labels = kmeans_cluster.labels_

result = cluster_centers[cluster_labels]
result = np.reshape(result, (img.shape))
cv2.imwrite('colormap.png', result)

# create masks and classification map
indexed = img.copy()
for i in range(k):
	sample = cluster_centers[i]

	mask = cv2.inRange(result, sample, sample)

	if b != 0:
		if not b % 2 != 0:
			b += 1
		mask = cv2.GaussianBlur(mask, (b, b), 0)

	cv2.imwrite(f'mask{i}.png', mask)

	indexed[mask>0] = (i, i, i)

cv2.imwrite('index_map.png', indexed)
