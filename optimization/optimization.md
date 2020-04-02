# The basics

__Optimization__ is the process of maximizing of profitable characteristics, and minimizing costs.


### Learn More

* [Unreal Engine 4 Optimization Tutorial](https://software.intel.com/en-us/articles/unreal-engine-4-optimization-tutorial-part-1)

## Benchmark

First, the __technological requirements__ must be specified. Next, you should _profile_ your game and identify a _bottleneck_.

### CPU or GPU bound?

Turn down all your graphical settings and/or turn down your resolution as low as possible. If that does not change your framerate, or does just a little, then your CPU is the bottleneck. But if the performance improves, then a GPU is the bottleneck.

[Identify Basic GPU/CPU Bound Scenarios](https://software.intel.com/en-us/gpa-cookbook-identify-basic-gpu-cpu-bound-scenarios)

Memory isn’t usually a bottleneck, but it can be. If you don’t have enough RAM, that can cause problems.

### Learn More

Intel GPA [guide](https://software.intel.com/en-us/articles/practical-game-performance-analysis-using-intel-graphics-performance-analyzers?elqTrackId=c1e06b59e39d48aaac871d9ad949f1ac&elqaid=20092&elqat=2)

* [Optimizing DayZ with Intel GPA - Buzz Workshop Portland, OR](https://www.youtube.com/watch?v=xdGDzH6S7gc)
* [UE4 Graphics Profiling: Intel Frame Analyzer](https://www.youtube.com/watch?v=lYMOm3tySNI)
* [Optimizations Enhance Just Cause 3 on Systems with Intel® Iris™ Graphics](https://software.intel.com/en-us/articles/optimizations-enhance-just-cause-3-on-systems-with-intel-iris-graphics)

# FPS vs MS

### Frames per second (FPS)

One of the most common benchmarks used in measuring the graphics performance of a video game is the [frame rate](https://en.wikipedia.org/wiki/Frame_rate) or frames per second. 

> FPS is the number of times the image on the screen is refreshed each second.

__However using FPS as the performance measurement is wrong most of the time.__ FPS measurement is not uniform and saying "performance increases by 5fps" when you talk about going up from 10 to 15fps means huge 33.34ms increase, while if you talk about 55 and 60 fps, it gives 1,5ms.

Having 60fps target, you have 16.67ms limit for all your processing.

The actual cost of features is a period of time, not a number of frames. 

### Milliseconds per frame (ms)

The inverse of the frames per second (FPS) gives us the seconds per frame (SPF); there are 1000 milliseconds in a second.
```
1000/fps = ms/frame
60fps means 1000/60 = 16.666ms per frame
```
While the frames per second increase, the number of milliseconds decreases at a slower rate:
```
90fps = 11.11ms - for VR to reduce motion sickness
60fps = 16.67ms - action games
50fps = 20ms
40fps = 25ms
30fps = 33.34ms - adventure, etc
20fps = 50ms
10fps = 100ms
```

__Example__: we have a scene running at 35fps - `1000/35 = 28.57ms`, let's say we want to use [HBAO+ Ultra](http://developer.download.nvidia.com/gameworks/events/GDC2016/atatarinov_alpanteleev_advanced_ao.pdf) that takes 4.8ms - `28.57 + 4.8 = 33.37ms`, that means our scene is now running at 30fps.

### Learn More

* [FPS vs MS](http://renderingpipeline.com/2013/02/fps-vs-msecframe/)

## How do we influence this

__FPS drops are caused by CPU and GPU taking longer time to process the frames.__

* For CPU, most demanding are _draw calls_, _positions_,  _math_ and _visibility_ (physics, AI, skeletal animations, projectiles, etc.)
* GPU is often limited by _fillrate_ or memory _bandwidth_. Typical problems are lighting, dynamic shadows or translucency.

### Polycount & LODs

A Level of Detail model ([LOD](http://wiki.polycount.com/wiki/LOD)) is a lower-resolution version of a game model. 

LOD0 is the original mesh, the higher the LOD the fewer vertices to be processed. This leads to big performance improvements by __reducing the cost on the CPU and GPU vertex processing__.

GDC [presentation](https://www.gdcvault.com/play/1017873/LOD-Techniques-for-Boosting-Rendering) from Simplygon about LODs and how they affect overshading.

General advises:

* Watch the number of vertices and faces of the models, check for the __polycount limits__. Reduce tris and remove polys of the model which are never visible.
* Make sure that all of the models have __LODs__ (Except the very simple ones like blocks). Look for your models LODs distances, for example you may have the model on such a distance where it's already 100px small on the screen but still is in LOD0 with 10k tris.
* Do not leave **hidden objects** and vegetation under terrain or inside other objects, and preferably terrain parts under objects. It wastes the CPU and GPU processing time for nothing.
* Make assets **modular**. Keep the number of different materials per scene low, and share as many materials between different objects as possible.
* Use **bilboards** on distance to fake detailed geometry. 

### Overshading

Overshading is caused by tiny or thin triangles and can really hurt performance by wasting a significant portion of the GPU’s time. Overshading is a consequence of how **GPUs process pixels in quads, blocks of 2x2 pixels**. It’s done like this so the hardware can do things like comparing UVs between pixels to calculate appropriate mipmap levels. [[3](https://www.gamasutra.com/blogs/KeithOConor/20170705/301035/GPU_Performance_for_Game_Artists.php)]

This means that if a triangle only touches a single pixel of a quad, the GPU still processes the whole quad and just throws away the other three pixels, **wasting 75% of the work**. [[3](https://www.gamasutra.com/blogs/KeithOConor/20170705/301035/GPU_Performance_for_Game_Artists.php)]

> Small triangles are bad for performance. 

Filling the frame buffer with anything larger than 16 by 16 tiles have no effect on the GPU performance. The primitive minimum size in pixels is pretty much the same for all vendors. Covering less than 8 by 8 pixels, with two triangles starts to have a significant impact on performance and it grows exponentially. [[4](https://www.g-truc.net/post-0662.html)]

> In the meantime, if we want some good primitive performances, let's set the minimum target to about 8 by 8 pixels per triangles on screen. [[4](https://www.g-truc.net/post-0662.html)]

Tiny triangles are also a problem because GPUs can only process and rasterize triangles at a certain rate, which is usually relatively low compared to how many pixels it can process in the same amount of time. With too many small triangles, it can’t produce pixels fast enough to keep the shader units busy, resulting in stalls and idle time – the real enemy of GPU performance. [[4](https://www.g-truc.net/post-0662.html)]

### Culling

[Culling explained](https://docs.cryengine.com/display/SDKDOC4/Culling+Explained) on Crytek docs.

Culling is completely excluding objects from processing when they are outside the view. This is an effective way to reduce both the CPU and GPU load.

When multiple meshes are merged into a single object, their individual bounding volumes must be combined into a single large volume that is big enough to enclose every mesh. This increases the likelihood that the visibility system will be able to see some part of the volume, and so will consider the entire collection visible. That means that it becomes a **draw call**, and so the vertex shader must be executed on every vertex in the object - even if very few of those vertices actually appear on the screen. This can lead to a lot of GPU time being wasted because the vertices end up not contributing anything to the final image. [[3](https://www.gamasutra.com/blogs/KeithOConor/20170705/301035/GPU_Performance_for_Game_Artists.php)]



### Opacity & Overdraw

Overdraw happens when the same __pixel is drawn multiple times__ (when objects are drawn on top of other).

The thing that impacts the __fillrate__ the most is __transparent__ stuff like particles with alpha blending. Limit the amount of opacity maps you use and their impact on the scene. If your map has a lot of opacity it’s better to add a few extra cuts and reduce the opacity area than to save a few polygons.

There's an [article](http://realtimecollisiondetection.net/blog/?p=91) on particle optimizations for the further reading



### Lighting & Shadows

Static lights are  the fastest, dynamic lights are more costly. Try to avoid lighting spheres or conuses to overlap each other. Reduce lights amount and cast distance as much as possible.

> Bake as much lighting effects as possible. 

Lights can optionally cast shadows. This gives them greater realism but has a **bigger performance cost**. Lights and realtime shadows have a big impact on performance, these effects give extra draw calls for the CPU and extra processing on the GPU. 

> Disable shadow casting where possible.

Soft shadows have a greater rendering overhead than hard shadows but __this only affects the GPU and does not cause much extra CPU work__. [[6](https://www.construct.net/en/blogs/construct-official-blog-1/remember-not-waste-memory-796)]


### Screen space effects

[Adaptive Screen Space Ambient Occlusion](https://software.intel.com/en-us/articles/adaptive-screen-space-ambient-occlusion)

### Physics

### Multithreading

[Why threading matters for Ashes of the Singularity](https://software.intel.com/en-us/articles/why-threading-matters-for-ashes-of-the-singularity)

### Intel Open Image Denoise

[Intel® Open Image Denoise: Optimized CPU Denoising | SIGGRAPH 2019 Technical Sessions](https://www.slideshare.net/IntelSoftware/intel-open-image-denoise-optimized-cpu-denoising)

high-performance, open-source filter for images rendered with ray tracing.


# DIP

CPU is often limited by the number of batches that need to be rendered. `[5]`

> Dip - DrawIndexedPrimitives. DrawElements in OpenGL

Draw call commands are given by CPU to GPU, to render a mesh. The command only points to a mesh which shall be rendered and doesn’t contain any material information. After the command is given, the GPU takes the render state values (material, textures, shaders etc…) and all the vertex data to convert this information into pixels on your screen. `[13]`

> Every mesh with a different material will require a separate Draw Call. `[13]`

Reducing Draw Calls will reduce overhead for the GPU and clearing up CPU usage for other processing.

> If your frame rate is fine, there is no need to worry about Draw Calls.

If you're not bound on Draw Calls, it's better not to reduce them as that affects culling, making it less precise.

## How do we influence this

The main reason to make fewer draw calls is that GPUs can transform and render triangles much faster than you can submit them. If you submit few triangles with each call, the CPU won't be able to feed the GPU fast enough and the GPU will be mostly idle. [15 - actually is also quoted from forum discussion] But also, if the mesh exceeds the vertex limit for a single batch, then it will be split into more than one batch, and cause more draw calls.

Try to keep the number of UV mapping seams and hard edges (doubled-up vertices) as low as possible.

Note that the actual number of vertices that graphics hardware has to process is usually not the same as the number reported by a 3D application. Modeling applications usually display the number of distinct corner points that make up a model (known as the geometric vertex count). For a graphics card, however, some geometric vertices need to be split into two or more logical vertices for rendering purposes. A vertex must be split if it has multiple normals, UV coordinates or vertex colors. `[8]`

> Do not make too many too trivial shapes.

Do not make millions of shapes with only a few vertices. Merge your shapes to have thousands of triangles in a single shape. 

BUT:

> Do not make too few shapes.

This one is explained above in the culling section.

Each shape is passed as a whole, and shapes may be culled. By using only a few very large shapes, you make this **culling worthless**. (In most cases you would not want to combine all the telephone poles into a single model, because then the renderer couldn't cull the unseen meshes, so ALL the triangles would have to be loaded.) `[2]`

> Draw calls often have a more significant impact on performance than polycount.

Which means if you need some extra polys to make a model smoother - go for it.

Even if using different meshes and producing multiple draw calls, **you can improve performance by avoiding multiple materials, and grouping multiple textures on a single atlas** to avoid switching texture maps (which causes Render State changes with extra Draw Calls).

> Note that combining two objects which don’t share a material does not give you any performance increase at all.

Nice [presentation](https://www.nvidia.com/docs/IO/8228/BatchBatchBatch.pdf) from NVidia on batching.

> GPU Idle? Add Triangles For Free! 

> GPU Idle? Complicate Pixel Shaders For Free!

# VRAM

VRAM only store image data the GPU needs to render the frame:

* Shader Programs
* Vertex Buffers
* Index Buffers
* Textures

## How do we influence this

Textures impact the _bandwidth_ the most. There are ways to optimize them to increase the speed and lower GPU memory usage:

* texture compression
* scale down textures
* [mipmaping](https://en.wikipedia.org/wiki/Mipmap)
* [texture atlases](https://en.wikipedia.org/wiki/Texture_atlas)
* [channel packing](http://wiki.polycount.com/wiki/ChannelPacking)

### Texture compression

Popular compressed formats like PNG and JPG cannot be decoded directly by the GPU. Before images are loaded into memory they must first be converted to a format that can be quickly accessed by the GPU. This involves creating mip-maps and either compressing the image so it takes up less video memory or leaving it uncompressed. [11]

A better option is to use hardware accelerated formats designed for the GPU. This means that they do not need to be decompressed before being copied and results in decreased loading times for the player and may even lead to increased performance due to hardware optimizations. [12]

The formats designed for the GPU:

* [S3TC](https://en.wikipedia.org/wiki/S3_Texture_Compression) (DXT) - the oldest and most common format
* [ETC](https://en.wikipedia.org/wiki/Ericsson_Texture_Compression) - this one is for android and not supported by iOS
* [PVRTC](https://en.wikipedia.org/wiki/PVRTC) - for iOS, but can also be used on android and PC
* [ASTC](https://en.wikipedia.org/wiki/Adaptive_Scalable_Texture_Compression) - similar to DXT, but you can choose the size of blocks like 4 x 4 or 12 x 12. It ranges from 8 bpp to less than 1 bpp. 

### Texture size and bpp

If you're using common formats that are not designed for direct GPU access, they are __decompressed to their full size in memory__ for rendering, which means your few-kb 8bit PNG file of size 2048x2048 will take up 4mb in memory.

> Playing with your image formats only affects the download size - it does not affect memory use. 

So what size a pixel actually is? It measures in  [bits per pixel](https://en.wikipedia.org/wiki/Color_depth) (__bpp__) and depends on how much color we store:

`1 bit per pixel = 2 colors  // either white or black`

As we have 2 values in 1 bit, then to calculate the rest we have - `2 in the power of bpp`

```
2 bpp = 4 colors
4 bpp = 16 colors
8 bpp = 256 colors // Low Color
16 bpp = 65,536 colors // High Color
24 bpp = 16,777,216 colors  // True Color
```

> Color Depth, also known as _bit depth_, is either the number of bits used to indicate the color of a single pixel, or the number of bits used for each color component of a single pixel. When referring to a _pixel_, the concept can be defined as _bits per pixel_ (**bpp**), which specifies the number of bits used. When referring to a _color component_, the concept can be defined as _bits per component_, bits per channel, bits per color (all three abbreviated **bpc**) [20]

__RGB 24bit__ gives us 8 bits per channel (R8G8B8), but there's no alpha, by adding it, we get **RGBA 32bit** (R8G8B8A8). 

__RGB 16bit__ is actually 5 bits per channel (R5G6B5) with one extra bit in the green channel, where it matters most, because human eyes are better in seeing in green spectrum. **RGBA 16bit** has 4 bits per channel (R4G4B4A4).

Calculating the actual texture storage size is simple: `width * height * bpp`

For example, we have 1k texture with 16 bits per pixel:
```
1024 * 1024 * 16 = 16777216 bits,
16777216 / 8 = 2097152 bytes (converted bits to bytes),
2097152 / 1024 = 2048 kb (converted bytes to kilobytes),
2048 / 1024 = 2 Mb (converted kilobytes to megabytes).
```

That means our texture is going to take 2Mb of VRAM.


### BC1..3 (DXT1..5)

> DXT compression works with texels and each texel is a _4x4 block_ of pixels, DXT can't work with an image with a dimension smaller than 4.

* Uncompressed
* **BC1 (DXT1)** - RGB(5:6:5), 4 bpp, no alpha or 1 bit (black or white) alpha, 8:1 compression ratio
* **BC2 (DXT2/DXT3)** - RGBA(8:8:8:4), 8 bpp, with 4bit alpha, 4:1 compression ratio
* **BC3 (DXT4/DXT5)** - RGBA(8:8:8:8), 8 bpp, with 8bit alpha, 4:1 compression ratio
* **BC3n(DXT5)** - 8 bpp, specifically for normal maps

### MIP Maps

MIP Maps are used for LOD. When rendering textures on models far from the camera, MIP Maps improve performance by using pre-scaled-down versions of textures. They are intended to increase rendering speed and reduce aliasing artifacts, improving image quality. 


### Texture Atlases

An Nvidia paper - [Improve Batching Using
Texture Atlases](http://download.nvidia.com/developer/NVTextureSuite/Atlas_Tools/Texture_Atlas_Whitepaper.pdf)


# Memory

__write about cache, ram access here__

Texture files are uploaded at runtime from system RAM to VRAM, so the graphics data is temporarily in both places.

Reducing the memory is good not only on the storage size itself but also __saves CPU time__ on loading from memory.

## How do we influence this

Reuse assets, do modular assets that you can combine different ways to make variations, instead of creating lots of unique ones, which can eat a lot of memory.



### Collisions

If you have too precise collisions it can eat a lot of memory, collision that was generated from the model itself and spawned across the map, may take dozens of MB (and take really huge amount of time on CPU processing). It's preferable to make as simple collision shapes as possible.

The relative costs of collision detection, from most expensive to least: 
1. mesh
1. convex hull
1. sphere
1. box
1. plane
1. point

* [Real-Time Collision Detection](https://www.amazon.com/exec/obidos/tg/detail/-/1558607323?tag=realtimecolli-20)

### Havok Destruction



### Audio

> There are a few platforms that always use a specific type of compression, such as HEVAG for the PS Vita, XMA for XBox One, and AAC for WebGL. (quoted from Unity 2017 Game Optimization book)


* Reduce the amount of the audio clips playing simulatinously to reduce the CPU load/
* Force audio to mono if there's no need in stereo effect
* Resample to lower frequencies

Streaming should be restricted to large files. Runtime hard disk acess is one of the slowest forms of data access.

# Links

1. [FPS vs msec/frame](http://renderingpipeline.com/2013/02/fps-vs-msecframe/)
2. [Optimization and profiling](https://castle-engine.io/manual_optimization.php)
3. [GPU Performance for Game Artists](https://www.gamasutra.com/blogs/KeithOConor/20170705/301035/GPU_Performance_for_Game_Artists.php)
4. [How bad are small triangles on GPU and why?](https://www.g-truc.net/post-0662.html)
5. [Optimizing graphics performance](https://docs.unity3d.com/Manual/OptimizingGraphicsPerformance.html)
6. [Light troubleshooting and performance](https://docs.unity3d.com/Manual/LightPerformance.html)
7. [Batch, Batch, Batch](https://www.nvidia.com/docs/IO/8228/BatchBatchBatch.pdf)
8. [Beautiful, Yet Friendly Part 2: Maximizing Efficiency](http://www.ericchadwick.com/examples/provost/byf2.html)
9. [Optimizing the rendering of a particle system](http://realtimecollisiondetection.net/blog/?p=91)
10. [System RAM and VRAM Explained](https://jacksondunstan.com/articles/2068)
11. [Texture Compression](http://docs.garagegames.com/torque-3d/official/content/documentation/Artist%20Guide/Formats/TextureCompression.html)
12. [A Simple How To Guide For Graphics Optimization In Unity](http://www.theappguruz.com/blog/graphics-optimization-in-unity)
13. [How To Make Your Games Run Superfast By Using Draw Call Reduction](http://www.theappguruz.com/blog/learn-draw-call-reduction-and-make-your-games-run-superfast)
14. [Performance Guidelines for Artists and Designers ](https://docs.unrealengine.com/en-US/Engine/Performance/Guidelines/index.html)
15. [Render Hell 2.0](https://simonschreibt.de/gat/renderhell/)
16. [Remember not to waste your memory](https://www.construct.net/en/blogs/construct-official-blog-1/remember-not-waste-memory-796)
17. [Chapter 28. Graphics Pipeline Performance](https://developer.download.nvidia.com/books/HTML/gpugems/gpugems_ch28.html)
18. [Unite 2012 - Performance Optimization Tips and Tricks for Unity](https://www.youtube.com/watch?v=jZ4LL1LlqF8&feature=youtu.be&t=1254)
19. [Texture formats for 2D games, part 1](http://joostdevblog.blogspot.com/2015/11/texture-formats-for-2d-games-part-1.html)
20. [Texture formats for 2D games, part 3: DXT and PVRTC](http://joostdevblog.blogspot.com/2015/11/texture-formats-for-2d-games-part-3-dxt.html)
21. [Color depth](https://en.wikipedia.org/wiki/Color_depth)
22. [Texture Compression Techniques](http://sv-journal.org/2014-1/06/en/index.php?lang=en)