# nvDXT

It's included in **Nvidia DDS** utilities, you can download it [here](https://developer.nvidia.com/legacy-texture-tools)

* reads .tga, .bmp, .gif, .ppm, .jpg, .tif, .cel, .dds, .png, .psd, .rgb, .bw and .rgba
* compresses images
* writes out .dds file
* filters MIP maps
* does batch processing
* It also can read a profile created from the Photoshop plugin

## batch converter

Here's a batch [script](https://github.com/shinsoj/techart/blob/master/dds_converter/dds_converter.cmd), it converts TGA found in the current folder into DDS. You need to put this file and **nvdxt.exe** into your TGA's folder.

## nvDXT parameters
You can view the full list of options by running a cmd file (from the folder with nvdxt in it) with this code:
``` bat
nvdxt.exe
pause
```
**Input - output**:
``` bat
-file [file name with or without directory] & :: input file to process
-deep [directory] & :: include all subdirectories
-outdir [directory] & :: output directory
```
My example code converts all tga files found in the current folder,
to specify the **file name and location**, write something like this:
``` bat
-file c:\temp\myfile.tga
```
or
``` bat
-file c:\temp\*.tga
```
My example code saves the dds files to the current folder,
to specify the **output folder**, write something like this:
``` bat
-outdir c:\temp\
```

**Quality**:
``` bat
-quick & :: use fast compression method
-quality_normal & :: normal quality compression
-quality_production & :: production quality compression
-quality_highest & :: highest quality compression (this can be very slow)
```

**Texture formats** (default is DXT3):
``` bat
-dxt1a & :: 1bit alpha, fewer colors than dxt1c, only for special cases
-dxt1c & :: use same compression as dxt3/5 but no alpha channel
-dxt3 & :: 4bit uncompressed alpha channel that means only 16 level
-dxt5 & :: compressed alpha channel allows 256 levels, the best format for textures with alpha channel
```

**Mip maps**:
``` bat
-nomipmap - do not generate mipmaps
-nmips <integer> - mipmap levels amount
```

Mip map **filtering** options (default is box filter):
``` bat
-Point
-Box
-Triangle
-Quadratic
-Cubic & :: the best compromise of performence and quality
-Catrom
-Mitchell
-Gaussian
-Sinc
-Bessel
-Hanning
-Hamming
-Blackman
-Kaiser
```

If you want to only convert files which **timestamp** has changed (if you only changed a single texture for example), use this option:
``` bat
-timestamp
```

Read a **profile** created in Photoshop (you can simply create a profile and set no other options but input-output):
``` bat
-profile <profile name>
```
