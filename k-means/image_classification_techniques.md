# Creating masks with image classification techniques

Here's my script: __[k-means_classification.py](https://github.com/shinsoj/techart/blob/master/k-means/k-means_classification.py)__

It uses _unsupervised K-Means_ method to create masks out of the satellite image for fast terrain prototyping.

To run it you need to install Python (with checkbox __Add Python to PATH__)
and then install libraries, just by running this with cmd:

```
python -m pip install numpy matplotlib opencv-python sklearn
```

Its input is _input.png_, output includes:
* colormap.png
* index_map.png, where each tone = number of the mask
* mask[0...n].png

![example](https://github.com/shinsoj/techart/blob/master/k-means/img/img1.jpg)

If you need supervised methods with more control and precision, you can use QGis with some plugins or try ENVI or ArcGis.

## What is image classification

It's an approach to set classes (like forest, field, water, etc) to pixels, making a map of areas of different types. In the case of gamedevelopment, we can use it to create masks for textures for a terrain.

There are three techiques:
* unsupervised
* supervised
* object-based

### Unsupervised image classification

This one is the most basic one, it clusters pixels and sets classes to them. Ome of the common clustering methods is [K-Means](https://en.wikipedia.org/wiki/K-means_clustering). You identify the number of clusters you wish to generate and alorithm does the work.

### Learn more

If you want to learn more about this theme, you can start with these links. 

* [Image Classification Techniques in Remote Sensing](http://gisgeography.com/image-classification-techniques-remote-sensing/) 
* [Image Classification](https://earth.esa.int/landtraining09/D2L2_Caetano_Classification_Techniques.pdf) - presentation with methodics
* [Supervised and Unsupervised Classification in Remote Sensing](https://gisgeography.com/supervised-unsupervised-classification-arcgis/)
* [Remote sensing applications](https://en.wikipedia.org/wiki/Remote_sensing_application) 

From proprietary software ENVI is comfy to work with, but there's also a free option - __QGis__ with plugins.

Links to data:

* http://gisgeography.com/free-satellite-imagery-data-list/ - satellite
* http://gisgeography.com/top-6-free-lidar-data-sources/ - lidar
* http://gisgeography.com/best-free-gis-data-sources-raster-vector/ - gis data, raster, vector
* http://gisgeography.com/free-global-land-cover-land-use-data/ - land cover, land use

The __[land covers](https://en.wikipedia.org/wiki/Land_cover)__ are created using the methods described above.
* [9 Free Global Land Cover / Land Use Data Sets](https://gisgeography.com/free-global-land-cover-land-use-data/)

## Masks using QGis with Orfeo (option 2, just in case)

### Installing QGis and Orfeo toolbox

1. Download [QGis](https://www.qgis.org/en/site/forusers/download.html) and install it.
1. Download [OTB](https://gitlab.orfeo-toolbox.org/orfeotoolbox/qgis-otb-plugin) plugin as archive, unpack and put it into this folder
```
C:\Users\%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
```
1. Download [Orfeo](https://www.orfeo-toolbox.org/), unpack, rename the folder into `Orfeo` and replace it to `C:\`
1. Go to `Settings - Options - Processing - Providers - OTB` and set it up:
	1. Activate = `V`
	1. OTB application folder = `C:/Orfeo/lib/otb/applications`
	1. OTB folder = `C:/Orfeo/`

### Creating a classification map

1. Open Processing Toolbox `Ctrl+Alt+T`
1. Run `OTB > KMeansClassification`
1. Choose *Input image*, *Number of classes* and *Output image*
1. Press `Run` and after some time you can see the index map, it's already saved to the folder you've chosen.
