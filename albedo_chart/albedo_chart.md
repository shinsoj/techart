
# Color space conversions

The formula for converting _sRGB to linear_:
```
If (0 ≤ S ≤ 0.04045):
	L = S/12.92
Else (0.04045 < S ≤ 1):
	L = ((S+0.055)/1.055)^2.4
```
And _Linear to sRGB_:
```
If (0 ≤ L ≤ 0.0031308):
	S = L * 12.92
Else (0.0031308 < L ≤ 1):
	S = 1.055*L^(1/2.4) - 0.055
```
The formulas below are simplified approximations of converting _sRGB to Linear and the reverse_, which should give good enough results in most cases (it gives larger relative errors in darker regions but that's where the eyes are less sensitive):
```
Linear = ((sRGB / 255) ^ 2.2) * 255
sRGB = ((Linear / 255) ^ 0.4545) * 255
```

Here's some explanation, where the values are coming from:
* `2.2` - this is gamma
* `0.4545 = 1 / 2.2` - this is an inverse of gamma
* `X / 255` - this means _normalizing_ the value (convert from 0-255 range to 0-1)

To check the albedo of your texture (in sRGB space) we should separate the channels:
```
Albedo = ((R/255)^2.2 + (G/255)^2.2 + (B/255)^2.2) / 3
```

For example, color-pick:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/01.jpg)

And calculate, for this example we have `0.27` albedo value (with some error):
```
((0/255)^2.2 + (168/255)^2.2 + (170/255)^2.2) / 3 = 0.27
```

> To avoid doing any calculations, you can check the value in Photoshop and Substance Designer.


## How to check albedo value in Substance Designer

Use this Function that converts sRGB to Linear:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/08.jpg)

This function is used inside the __Pixel Processor__ node which samples the input and converts each channel separately:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/09.jpg)

Pointing at the color with cursor in 2D view you can see it's value in float. For our example color we did before, it's `0.262745`:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/04.jpg)


## How to check albedo value in Photoshop

Add __Exposure correction__ layer with __Gamma Correction__ set to `0.4545`:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/05.jpg)

Then, add __Channel Mixer__ layer, check the __Monochrome__ box and set all channels to `33%`

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/06.jpg)

With color picker you can see the albedo value, which in this case is `26%` for our example above:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/07.jpg)


# Albedo values

Gathered from all around the web, values are for the reference and general idea of how dark\light the common material usually is.

For __NonMetals__, the darkest albedo is carbon with __0.04__ value, the brightest are the white paint and fresh snow with values around __0.8 (inside 60-240 sRGB range)__. 

__Values are in Linear RGB (float)__.

## NonMetal values

### Ground, sand, rock
* Carbon (Coal, forged iron) `0.04`
* Black soil, wet `0.08`
* Black soil, dry `0.15`
* Bare soil `0.17`
* Grey soil, wet `0.10` – `0.12`
* Grey soil, dry `0.25` – `0.30`
* Dry silt loam soil `0.23` – `0.28`
* Dry clay soil `0.15` – `0.35`
* Dry sandy soil `0.25` – `0.45`
* Dry salt cover `0.5`
* Wet sand `0.23`
* Dry sand `0.4`
* Yellow clay `0.16`
* Rock `0.3` – `0.4`

### Vegetation
* Conifer Forest `0.08` – `0.12`
* Deciduous trees `0.15` – `0.18`
* Tall wild grass `0.16` – `0.18`
* Short green grass `0.20` – `0.25`
* Grain crops `0.10` – `0.25`
* Corn field `0.16` – `0.17`
* Tea bushes `0.16` – `0.18`
* Summer foliage `0.09` – `0.12`
* Autumn foliage `0.15` – `0.3`
* Tundra `0.2`

### Snow, ice, water
* Melting snow (clean) `0.6` – `0.62`
* Ice `0.5` – `0.7`
* Ice, sea `0.3` – `0.45`
* Ice, glacier `0.2` – `0.4`
* Fresh snow `0.7` – `0.9`
* Water, sun near zenith `0.05`
* Water, sun near horizon `0.5` - `0.8`

### Asphalt
* New asphalt `0.04` – `0.05`
* Aged asphalt `0.1` – `0.18`
* Wet asphalt `0.06` – `0.08`
* Gravel `0.13`

### Roofs
* Tar & gravel `0.33`
* Corrugated roof `0.1` – `0.15`
* Red/Brown roof tiles `0.1` – `0.35`
* White asphalt shingle `0.2`

### Concrete
* Aged concrete `0.2` – `0.3`
* New concrete (traditional) `0.4` – `0.55`
* Polished concrete `0.55`
* New concrete with white portland cement `0.7` – `0.8`

### Wood
* Batten (fresh wood) `0.35` – `0.42`
* Batten (old, weathered) `0.12` – `0.16`
* Varnished wood `0.13`

### Tiles, bricks, finishings, etc
* Terracotta tile `0.28`
* Brick `0.2` – `0.4`
* Sandstone `0.18`
* Plaster `0.4` – `0.45`
* Magnesium oxide `0.96`
* White gypsum `0.85`
* Alabaster `0.92`
* Granite gray `0.35` – `0.40`

### Paint
* Black acrylic paint `0.05`
* White acrylic paint `0.8`
* Colored paint `0.15` – `0.35`

### Misc
* Forged Iron `0.04`
* Natural silk fabric `0.35` – `0.55`
* Skin `0.25` – `0.35`
* White paper sheet `0.6` – `0.7`


## Metal values

Metals albedo values are between `0.45` - `0.98` (__180-250 sRGB range__). Lower values are for matte, higher are for polished metal.

These sRGB values are for the reference, don't take them for granted.

* Iron  = `c4c7c7` (198, 198, 200)
* Brass = `d6b97b` (214, 185, 123)
* Copper = `fad0c0` (250, 208, 192)
* Gold = `ffe29b` (255, 226, 155)
* Aluminum = `f5f6f6` (245, 246, 246)
* Chrome = `c4c5c5` (196, 197, 197)
* Silver = `fcfaf5` (252, 250, 245)
* Cobalt = `d3d2cf` (211, 210, 207)
* Titanium = `c1bab1` (195, 186, 177)
* Platinum = `d5d0c8` (213, 208, 200)
* Nickel = `d3cbbe` (211, 203, 190)
* Zinc = `d5eaed` (213, 234, 237)
* Mercury = `e5e4e4` (229, 228, 228)
* Palladium = `ded9d3` (222, 217, 211)

# Useful links

* Here are some links at [Polycount](http://wiki.polycount.com/wiki/PBR)
* Allegorithmic PBR Guide [1](https://academy.substance3d.com/courses/the-pbr-guide-part-1) and [2](https://academy.substance3d.com/courses/the-pbr-guide-part-2)
* [Basics of PBR](https://www.youtube.com/watch?v=fePsD_8p9vM) by Ben Cloward
* [Video from SIGGRAPH](https://www.youtube.com/watch?v=j-A0mwsJRmk) 
* [Cubetutorials](https://www.youtube.com/watch?v=GVNnfZG4riw).


Also make sure to check this [post by Harrison Eilers](https://www.artstation.com/harrisoneilers/blog/ADnb/011-pbr-validate-for-ue4) about PBR validating in UE4 with a simple post process material.
