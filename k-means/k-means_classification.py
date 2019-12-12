import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import cv2

# set the number of masks
# k = 3

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 


k = inputNumber('How much masks do you want?: ')

# read
img = cv2.imread('example.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

image_2d = img.reshape((img.shape[0] * img.shape[1], 3))
img_r = (img / 255.0).reshape(-1, 3)

# supplying the number of clusters we wish to generate
# kmeans_cluster = KMeans(n_clusters=k) # this is slower but more accurate
kmeans_cluster = MiniBatchKMeans(n_clusters=k) 
kmeans_cluster.fit(image_2d) # clusters our list of pixels

cluster_centers = kmeans_cluster.cluster_centers_ # dominant colors array
cluster_labels = kmeans_cluster.labels_

result = cluster_centers[cluster_labels]
result = np.reshape(result, (img.shape))
cv2.imwrite('colormap.png', result)

indexed = img.copy()

# create masks and classification map
for i in range(k):
	sample = cluster_centers[i]

	mask = cv2.inRange(result, sample, sample)
	blur = cv2.GaussianBlur(mask, (3, 3), 0)

	cv2.imwrite(f'mask{i}.png', blur)

	indexed[mask>0] = (i, i, i)

cv2.imwrite('index_map.png', indexed)
