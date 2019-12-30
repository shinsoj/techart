# Creating masks with image classification techniques

## Intro

**Wiki** quote:
> **Remote sensing** is the acquisition of information about an object or phenomenon without making physical contact with the object. [[1](https://en.wikipedia.org/wiki/Remote_sensing)]

Some info:

* [Image Classification Techniques in Remote Sensing](http://gisgeography.com/image-classification-techniques-remote-sensing/) 
* [Image Classification](https://earth.esa.int/landtraining09/D2L2_Caetano_Classification_Techniques.pdf) - presentation with methodics
* [Remote sensing applications](https://en.wikipedia.org/wiki/Remote_sensing_application) 

From proprietary software ENVI is comfy to work with, but there's also a free option - **QGis** with plugins.

Links to data:

* http://gisgeography.com/free-satellite-imagery-data-list/ - satellite
* http://gisgeography.com/top-6-free-lidar-data-sources/ - lidar
* http://gisgeography.com/best-free-gis-data-sources-raster-vector/ - gis data, raster, vector
* http://gisgeography.com/free-global-land-cover-land-use-data/ - land cover, land use


The **land covers** are created using the methods described above.

In Global Mapper you can find them in *Select online Data Source - Land Cover*

## Creating masks the fast way

Say, you have a picture:

![example](https://github.com/shinsoj/techart/blob/master/k-means/example.png)

And you need some masks generated out of it, to put textures on the terrain.

Here's my script that does this very simply and fast way: **[k-means_classification.py](https://github.com/shinsoj/techart/blob/master/k-means/k-means_classification.py)**

To run it you need to install Python (with checkbox **Add Python to PATH**)
and then install libraries, just running this with cmd:

```
python -m pip install numpy matplotlib opencv-python sklearn
```

If you need supervised methods with more control and precision, you can use QGis with some plugins or try ENVI or ArcGis.

## Using QGis with Orfeo

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

