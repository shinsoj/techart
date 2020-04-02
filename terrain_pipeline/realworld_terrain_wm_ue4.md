
## Elevation data

Here are some __heightmap data resources__:

- [30-Meter SRTM Tile Downloader](https://dwtkns.com/srtm30m/) and [90m here](http://dwtkns.com/srtm/)
- [5 Free Global DEM Data Sources – Digital Elevation Models](https://gisgeography.com/free-global-dem-data-sources/)
- Open Topography [SRTM GL3 (90m)](http://opentopo.sdsc.edu/raster?opentopoID=OTSRTM.042013.4326.1) and [SRTM GL1 (30m)](http://opentopo.sdsc.edu/raster?opentopoID=OTSRTM.082015.4326.1)
- [SRTM Data](http://srtm.csi.cgiar.org/srtmdata/)

```
1 arc-second is approximately 30 meters per pixel
3 arc-seconds is approximately 90 meters per pixel
```

## QGis

[Download QGis](https://qgis.org/en/site/forusers/download.html)

### Extent select and export

Firstly we add a __Basemap__. For example Google Satellite:
```
https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}
```

Here is a list of popular XYZ tiles. Save it as XML file and import it in QGIS XYZ Tiles section:
```
<!DOCTYPE connections>
<qgsXYZTilesConnections version="1.0">
    <xyztiles zmin="0" password="" name="OpenStreetMap" authcfg="" username="" zmax="19" url="http://a.tile.openstreetmap.org/{z}/{x}/{y}.png" referer=""/>
    <xyztiles zmin="1" password="" name="Bing Virtual Earth" authcfg="" username="" zmax="19" url="http://ecn.t3.tiles.virtualearth.net/tiles/a%7Bq%7D.jpeg?g=1" referer=""/>
    <xyztiles zmin="0" password="" name="Cartodb Dark" authcfg="" username="" zmax="20" url="http://basemaps.cartocdn.com/dark_all/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="Cartodb Light" authcfg="" username="" zmax="20" url="http://basemaps.cartocdn.com/light_all/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI Terrain" authcfg="" username="" zmax="19" url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI Topo World" authcfg="" username="" zmax="19" url="http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI World Dark Gray" authcfg="" username="" zmax="19" url="http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI World Imagery" authcfg="" username="" zmax="19" url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI World Light Gray" authcfg="" username="" zmax="19" url="http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="ESRI World Ocean" authcfg="" username="" zmax="19" url="https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D" referer=""/>
    <xyztiles zmin="0" password="" name="Global Infrared" authcfg="" username="" zmax="19" url="http://realearth.ssec.wisc.edu/tiles/globalir/{z}/{x}/{y}.png" referer=""/>
    <xyztiles zmin="0" password="" name="Global Night Light" authcfg="" username="" zmax="19" url="http://realearth.ssec.wisc.edu/tiles/NightLightsColored/{z}/{x}/{y}.png" referer=""/>
    <xyztiles zmin="0" password="" name="Google Map" authcfg="" username="" zmax="19" url="https://mt1.google.com/vt/lyrs=m%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D" referer=""/>
    <xyztiles zmin="0" password="" name="Google Satellite" authcfg="" username="" zmax="19" url="https://mt1.google.com/vt/lyrs=s%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D" referer=""/>
    <xyztiles zmin="0" password="" name="Google Satellite Hybrid" authcfg="" username="" zmax="19" url="https://mt1.google.com/vt/lyrs=y%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D" referer=""/>
    <xyztiles zmin="0" password="" name="Google Terrain" authcfg="" username="" zmax="19" url="https://mt1.google.com/vt/lyrs=t%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D" referer=""/>
    <xyztiles zmin="0" password="" name="Google Terrain Hybrid" authcfg="" username="" zmax="19" url="https://mt1.google.com/vt/lyrs=p%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D" referer=""/>
    <xyztiles zmin="1" password="" name="NASA Night Black Marble" authcfg="" username="" zmax="19" url="http://realearth.ssec.wisc.edu/tiles/VIIRS-MASK-54000x27000/{z}/{x}/{y}.png" referer=""/>
    <xyztiles zmin="0" password="" name="OpenStreetMap Hot" authcfg="" username="" zmax="19" url="http://tile.openstreetmap.fr/hot/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="OpenStreetMap Monochrome" authcfg="" username="" zmax="19" url="http://tiles.wmflabs.org/bw-mapnik/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="Stamen Terrain" authcfg="" username="" zmax="20" url="http://tile.stamen.com/terrain/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="Stamen Toner" authcfg="" username="" zmax="20" url="http://tile.stamen.com/toner/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="Stamen Toner Lite" authcfg="" username="" zmax="20" url="http://tile.stamen.com/toner-lite/%7Bz%7D/%7Bx%7D/%7By%7D.png" referer=""/>
    <xyztiles zmin="0" password="" name="Stamen Water Color" authcfg="" username="" zmax="18" url="http://tile.stamen.com/watercolor/%7Bz%7D/%7Bx%7D/%7By%7D.jpg" referer=""/>
</qgsXYZTilesConnections>
```

__QRectangleCreator__ plugin

Layer - Create Layer - New Shapefile Layer, set the file name and __Geometry Type__ = `Polygon`

Create a polygon of desired size in meters (for example [2017x2017](https://docs.unrealengine.com/en-US/Engine/Landscape/TechnicalGuide/index.html)). Press the plugin's icon again to exit the edit mode.

Double-click the layer in Layers window, go to __Symbology__ and choose a style without fill, just the outline.

### Export

Drag'n'drop your srtm to qgis

the min-max values are needed for wm setup

turn off all the layers but the srtm one

Project - Import/Export - Export Map to Image

Calculate from layer

sve png

save satellite the same way

## World Machine

setup the map size, max/min = qgis layer values

File Import, click Place into Current View to fit the heightmap

now you may modify the heightmap and export it to Unreal

## Unreal Engine

[Landscape Technical Guide](https://docs.unrealengine.com/en-US/Engine/Landscape/TechnicalGuide/index.html)

### Material masks

[script link]

explain ue4 material setup here