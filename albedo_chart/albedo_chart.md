# PBR General

## Albedo \ Base Color

__A range for albedo \ diffuse color for non-metals is 60-240 sRGB.__ Do not set the value too dark, that's a common mistake, out of range values would not give enough of GI, breaking the lighting.

Metals need to have a reflectance range of 70-100% in the Base Color, that means that metals have range of 180-255 sRGB. Rougher the metal - darker the albedo, if Metallic has values lower than 0.8, not clearly metal, then the Base Color should be darker than it would be for pure metal.

## Roughness \ Glossiness

The __roughness__ texture controls the blurriness of the reflection. The rougher the surface, the blurrier the reflection. The roughness is the inverse of the __glossiness__. It has no technical constraints, this is completely artistical choice on how to represent this map, would it be polished or aged or having fingerprints, it is important for bringing realism to the material.

## Metalness

__Metallic maps use values of 0 - 1__, where metals are 1. Metallic map properties should represent the top layer of the material, for example dirty or painted metal which would not be metallic in this case.

## Specular

In Unreal Engine the __specular__ is a value that represents reflectiveness of a non-metal surface in the range of 0-8% (0.0-0.08), remapped to 0.0-1.0, where 0.5 = 4% reflective. Most non-metals have specular value between 2-5%, __it has no effect on metals__. Most of the materials reflect 4% of light, when looking strait at the surface, so just leave this value at default 0.5, that works for 99% of the materials. All Materials have specular, so it can't be 0 for physically correct surface.

We can modify specular if we want some small scale shadowing, in this case we would apply a __cavity__ map on it.

More info in [UE4 documentation](https://docs.unrealengine.com/en-US/RenderingAndGraphics/Materials/PhysicallyBased/#specular).


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

And calculate using the formula. For this example we have `0.27` albedo value (with some error):
```
((0/255)^2.2 + (168/255)^2.2 + (170/255)^2.2) / 3 = 0.27
```

> To avoid doing any calculations, you can check the value in Photoshop and Substance Designer.


## How to check albedo value in Photoshop

Simple way of checking texture value would be Luminosity in Histogram. Basically keep the textures in between the 80-240 range, roughly, the darkest albedo should be no less than 50-60 (I prefer keeping 55-60 as black surface):

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/luminosity.png)

If you want to convert sRGB color to linear space and see the linear albedo values, you can do this in a few steps:

1 - Add __Exposure correction__ layer with __Gamma Correction__ set to `0.4545`:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/05.jpg)

2 - Then, add __Channel Mixer__ layer, check the __Monochrome__ box and set all channels to `33%`

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/06.jpg)

3 - With color picker you can now see the albedo value, which in this case is `26%`:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/07.jpg)


## How to check albedo value in Substance Designer

It's easy to create a node for Albedo values validation:

1 - This Function converts sRGB to Linear:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/08.jpg)

2 - The function is used inside the __Pixel Processor__ node which samples the input and converts each channel separately:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/09.jpg)

3 - In 2D View, pointing at the color with cursor, you can see it's value in float. In this case it's `0.26`:

![example](https://github.com/shinsoj/techart/blob/master/albedo_chart/img/04.jpg)


# Albedo values

Gathered from all around the web, values are for the reference and general idea of how dark\light the common material usually is.

For __NonMetals__, the darkest albedo value is __0.04__ for carbon, the brightest are the white paint and fresh snow with values around __0.8__. That gives us 60-240 sRGB range. 

__Values are in Linear RGB (float)__.

## NonMetal values


| Surface | Albedo Linear | sRGB |
|---|---|---|
| __Ground, sand, rock__ | | |
| Dry salt cover | `0.5` | 186 |
| Dry sand | `0.4` | 168 |
| Rock | `0.3` – `0.4` | 148 - 168 |
| Dry sandy soil | `0.25` – `0.45` | 136 - 177 |
| Grey soil, dry | `0.25` – `0.30` | 136 - 148 |
| Dry silt loam soil | `0.23` – `0.28` | 131 - 143 |
| Wet Sand | `0.23` | 131 |
| Dry clay soil | `0.15` – `0.35` | 108 - 158 |
| Bare soil | `0.17` | 114 |
| Yellow clay | `0.16` | 111 |
| Black soil, dry | `0.15` | 108 |
| Grey soil, wet | `0.10` – `0.12` | 90 - 97 |
| Black soil, wet | `0.08` | 81 |
| Carbon (Coal, forged iron) | `0.04` | 59 |
| __Vegetation__ | | |
| Short green grass | `0.20` – `0.25` | 123 - 136 |
| Tundra | `0.2` | 123 |
| Tall wild grass | `0.16` – `0.18` | 111 - 117 |
| Tea bushes | `0.16` – `0.18` | 111 - 117 |
| Corn field | `0.16` – `0.17` | 111 - 114 |
| Deciduous trees | `0.15` – `0.18` | 108 - 117 |
| Autumn foliage | `0.15` – `0.3` | 109 - 148 |
| Grain crops | `0.10` – `0.25` | 90 - 136 |
| Summer foliage | `0.09` – `0.12` | 85 |
| Conifer Forest | `0.08` – `0.12` | 81 |
| __Wood__ | | |
| Batten (fresh wood) | `0.35` – `0.42` | 158 - 172 |
| Batten (old, weathered) | `0.12` – `0.16` | 97 - 111 |
| Varnished wood | `0.13` | 101 |
| __Snow, ice, water__ | |
| Fresh snow | `0.7` – `0.9` | 217 - 243 |
| Melting snow (clean) | `0.6` – `0.62` | 202 - 205 |
| Ice | `0.5` – `0.7` | 186 - 217 |
| Ice, sea | `0.3` – `0.45` | 148 - 177 |
| Ice, glacier | `0.2` – `0.4` | 123 - 168 |
| Water, sun near horizon | `0.5` - `0.8` | 186 - 230 |
| Water, sun near zenith | `0.05` | 65 |
| __Asphalt__ | | |
| Gravel | `0.13` |
| Aged asphalt | `0.10` – `0.18` | 90 - 117 |
| Wet asphalt | `0.06` – `0.08` | 71 - 81 |
| New asphalt | `0.04` – `0.05` | 59 - 65 |
| __Roofs__ | | |
| Tar & gravel | `0.33` | 154 |
| White asphalt shingle | `0.2` | 123 |
| Red/Brown roof tiles | `0.1` – `0.35` | 90 - 158 |
| Corrugated roof | `0.1` – `0.15` | 90 - 108 |
| __Concrete__ | | |
| New concrete with white portland cement | `0.7` – `0.8` | 217 - 230 |
| New concrete | `0.40` – `0.55` | 168 - 194 |
| Polished concrete | `0.55` | 194 |
| Aged concrete | `0.2` – `0.3` | 123 - 148 |
| __Tiles, bricks, finishings, etc__ | | |
| Alabaster | `0.92` | 246 |
| White gypsum | `0.85` | 237 |
| Plaster | `0.40` – `0.45` | 168 - 177 |
| Granite gray | `0.35` – `0.40` | 158 - 168 |
| Terracotta tile | `0.28` | 143 |
| Brick | `0.2` – `0.4` | 123 - 168 |
| Sandstone | `0.18` | 117 |
| __Paint__ | | |
| White paint | `0.8` | 230 |
| Colored paint | `0.15` – `0.35` | 108 - 158 |
| Black paint | `0.05` | 65 |
| __Misc__ | | |
| Magnesium oxide | `0.96` | 250 |
| White paper sheet | `0.6` – `0.7` | 202 - 217 | 
| Natural silk fabric | `0.35` – `0.55` | 158 - 194 |
| Skin | `0.25` – `0.35` | 136 - 158 |
| Forged Iron | `0.04` | 59 |

## Metal values

Metals have range of 180-255 sRGB. Rougher the metal - darker the albedo, if Metallic has values lower than 0.8, not clearly metal, then the Base Color should be darker than it would be for pure metal.

These __sRGB values__ are for the reference.

| Metal | Hex | RGB |
| --- | --- | --- |
| Iron  | `c4c7c7` | (198, 198, 200) |
| Brass | `d6b97b` | (214, 185, 123) |
| Copper | `fad0c0` | (250, 208, 192) |
| Gold | `ffe29b` | (255, 226, 155) |
| Aluminum | `f5f6f6` | (245, 246, 246) |
| Chrome | `c4c5c5` | (196, 197, 197) |
| Silver | `fcfaf5` | (252, 250, 245) |
| Cobalt | `d3d2cf` | (211, 210, 207) |
| Titanium | `c1bab1` | (195, 186, 177) |
| Platinum | `d5d0c8` | (213, 208, 200) |
| Nickel | `d3cbbe` | (211, 203, 190) |
| Zinc | `d5eaed` | (213, 234, 237) |
| Mercury | `e5e4e4` | (229, 228, 228) |
| Palladium | `ded9d3` | (222, 217, 211) |


