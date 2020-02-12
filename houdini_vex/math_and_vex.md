Houdini
======

- Some tricks to know - [HOUDINI BAG OF TRICKS](https://houdinitricks.com/houdini-bag-of-tricks/)
- [Points and Verts and Prims](http://www.tokeru.com/cgwiki/index.php?title=Points_and_Verts_and_Prims)

VEX basics
------

- SideFX Documentation about [VEX](https://www.sidefx.com/docs/houdini/vex/snippets.html).
- Series of lessons about VEX: [JoyOfVex](http://www.tokeru.com/cgwiki/index.php?title=JoyOfVex)
- [Vex Attributes vs Variables](https://houdinitricks.com/vex-attributes-vs-variables/)
- [Few gotchas when writing vex](https://houdinitricks.com/few-gotchas-when-writing-vex/)

Attributes have `@` before the name. Each statement must end with a semicolon `;`. To get the attribute, type:

```csharp
@Cd = @N; //  Cd for color and N for normal
@Cd = @N.y; // take only y (green channel) of the normal
@Cd = set (1,0,0); // set the value for each channel manually
```

To define your own attribute it works the same:

```csharp
@my_attribute = 1;
```

The attribute by default is `float`. For the other types, write the appropriate prefix:

```csharp
v@vector_attribute = {1,2,3}; // curly braces for numbers

i@integer_attribute = 2;

p@quaternion_attribute;  // quaternion
3@matrix_attribute; // 3x3 matrix

3@my_matrix = ident(); // you defined an identity matrix, so you can see nine matrix attributes in your Geometry Spreadsheet
```

> Don't forget telling the type when acessing your custom attribute as well, not only when defining it, or Houdini will treat is as a float any way.


Use __set()__ to define varying attributes:
```csharp
v@vector_attribute = set(N.x,0,1);
```

Defining __variable__:

```ruby
matrix3 my_matrix = ident();
```

Defined variables are used furter in the code without `@` prefix.


### Wrangle UI Controls

- SideFX Documentation about [Spare Parameters](https://www.sidefx.com/docs/houdini/network/spare.html).

```ruby
@scale_control = ch('scale');
```

In "Edit parameter interface" you can set the paramenter as you need, for example if you set the vector attribute:

```ruby
v@my_color = chv('color_sampler');
```

Then go to parameter interface, choose your parameter, change Type to Color and Show Color as "RGB Sliders"



Vectors
------

Good video about [Vectors](https://www.youtube.com/watch?v=tnDqwcNG20Y)

- __Magnitude__ is the length of the vector.
- __Direction__ is which way the vector is pointing.

3D vector is `float3` value [x, y, z]

### Vector addition and substraction

```
A + B = (A.x + B.x, A.y + B.y, A.z + B.z) = C
```

Addition of vectors is like chaining them tip to tail. The result then is a vector from tail of the first one to tip of the last one.

This gives us a __tangent__ vector:

```ruby
v@tangent_vector = (normalize(normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum)) + normalize(point(0, "P" , @ptnum) - point(0, "P" , @ptnum - 1))));

@N = v@tangent_vector;
```

__Negating__ a vector:

```
-[x y z] = [-x -y -z]
-[2 0 -5] = [-2 0 5]
```

Substracting is often used to find __relative distance__ between two points. By substracting point B from A, we get C, which represents B as if vector AB was set to origin (A = 0):

```
C = A - B
```

We can set __normals along curve__ with that:

```ruby
v@along_curve = normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum));
@N = v@along_curve;
```

If a curve is not closed, you can fix the _last point direction_ by inverting the vector towards the previous point:

```ruby
if (@ptnum != npoints(0)-1)
    @N = normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum));
else
    @N = normalize(point(0, "P" , @ptnum) - point(0, "P" , @ptnum - 1));
```


### Vector multiplication and division 

__Multiplying__ a vector by a scalar (__scaling__ a vector):

```
a[x y z] = [ax ay az]
2[1 3 0] = [2 6 0]
```

Vector __magnitude__ (length):

```
||v|| = sqrt(square(v.x) + square(v.y) + square(v.z))
```

In vex:

```ruby
@magnitude = length(@myVector);
```

Dividind a vector by it's lenght is __normalizing__ a vector. The resulting vector will have a _length of 1_, which calls a __unit vector__ (unit vector = vector / magnitude):

```
unit v = v / ||v||
```

```ruby
@myVector = normalize(@someVector);
```

### Dot product (scalar product)

Dot product produces a scalar value.

```
a ⋅ b = [a1 a2 a3] ⋅ [b1 b2 b3] = a1b1 + a2b2 + a3b3

[2 1 5] ⋅ [0 3 2] = 0 + 3 + 10 = 13
```
```
a ⋅ (b + c) = a ⋅ b + a ⋅ c
```

* `A • B = 1` when the unit vectors are _parallel_
* `A • B = -1` when the unit vectors point in _opposite direction_
* `A • B = 0` when the unit vectors are orthogonal (_perpendicular_)

With the dot product you can find the __angle between two vectors__:

```
θ = arccos(unit a ⋅ unit b)
```

In vex:

```ruby
v@unit_a = normalize(point(0, "P" , @ptnum - 1) - point(0, "P" , @ptnum));
v@unit_b = normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum));

@angle = degrees(acos(dot(v@unit_a, v@unit_b)));
```

With the dot product we also can find out _if some point is in the field of view_, for example. Say, we have a camera at point A(1, 3) looking in the B(1, 1) direction with 180 degrees fov, and we have some point P(3, 2):

```
V = P - A = (2, -1)
B • V = 1
```

So, the point P is in the field of view of A, because 1 > 0.

__Back-face detection__ is simply the dot product of the surface normal against incoming light (both normalized):

```
N ⋅ L = (N.x ⋅ L.x) + (N.y ⋅ L.y) + (N.z ⋅ L.z)
```


### Cross Product (vector product)

Cross product produces a vector value. The cross product creates a vector perpendicular to the original two vectors. If you change the vectors order, the result changes it's direction to the opposite.

```
A x B = C

|Ax|   |Bx|   |AyBz - AzBy|
|Ay| x |By| = |AzBx - AxBz|
|Az|   |Bz|   |AxBy - AyBx|
```

You can find a __triangle's normal__ based on two of it's edges.

Having normal along curve and tangent we can get the perpendicular vector (__up vector__) using the cross product.

```ruby
v@along_curve = normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum));

v@tangent_vector = (normalize(normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum)) + normalize(point(0, "P" , @ptnum) - point(0, "P" , @ptnum - 1))));

@N = normalize(cross(v@along_curve, v@tangent_vector));
```

We may now get the perpendicular vector to the tangent and up vectors, this one will always point outside the spline. You can build a spiral staircase with that, for example.

```ruby
v@along_curve = normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum));

v@tangent_vector = (normalize(normalize(point(0, "P" , @ptnum + 1) - point(0, "P" , @ptnum)) + normalize(point(0, "P" , @ptnum) - point(0, "P" , @ptnum - 1))));

v@up_vector = normalize(cross(v@along_curve, v@tangent_vector));

@N = cross(v@up_vector, v@tangent_vector);
```


### Visualizers

To visualize our vectors, RMB on Vizualizers > press on the plus (+) icon in Scene group, choose Marker and set it's style to `Vector` and attribute as your attribute name, in our case there are `tangent_vector` and `up_vector`, you can see kind of individual coordinate guides at each point now:




Matrices
------

Matrix from N and Up vectors
```ruby
matrix3 matrx = ident();
matrx = maketransform(@N,@up);
```

Quaternion from matrix:
```ruby
@orient = quaternion(matrx);
```

Matrix 4x4 from quaternion:
```
4@myTransform = qconvert(@orient);
```

* [Read about quaternions](http://www.tokeru.com/cgwiki/index.php?title=JoyOfVex17)
* [3blue1brown - What are quaternions](https://www.youtube.com/watch?v=d4EgbgTm0Bg)
