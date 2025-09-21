
# protopng protocol - v1

At it's heart a protopng is protobuf being sent over-the-wire inside a PNG. With this the wording here assumes knowledge of the [protobuf 3 specifications](https://protobuf.dev/programming-guides/encoding/) and the [PNG specifications](https://www.w3.org/TR/2003/REC-PNG-20031110/) ; these will be referenced during this document where possible.

## protopng file
A protopng file is purposely "just a PNG" to allow maximum compatibility with browsers, caching and other file handling processes on the internet. In this respect the protocol is the method of embedding our payload into a standard PNG. To mention, this process is not [Steganography](https://en.wikipedia.org/wiki/Steganography) as we are not trying to hide our payload within an existing image; instead it is more of a non-malicious [Trojan Horse](https://en.wikipedia.org/wiki/Trojan_Horse) situation.


### File Extension
`.png`


### File Structure
We use three standard [PNG Chunks](https://www.w3.org/TR/2003/REC-PNG-20031110/#11Critical-chunks) to form a valid PNG file.
```
+--------------------+
| IHDR | IDAT | IEND |
+--------------------+
```

#### IHDR
We create a very simple IHDR with these selected values:
```
+----------------------------------------------------------------------------------+
| Width | Height | Bit Depth | Colour  Type | Compression |   Filter   | Interlace |
+----------------------------------------------------------------------------------+
| Details below  |   8 bit   | 2 Truecolour |  0 Deflate  | 0 Adaptive |  0 None   |
+----------------------------------------------------------------------------------+
```

##### Width and Height Calculation
The method used to calculate a good pixel `height` and `width`. This is done to create a more evenly sized image as some browsers do not like super-wide or super-tall images.
**Note :** The concept here of the `transport-payload` is defined within the `IDAT` section below
```
wrapped_length = length in bytes of the transport-payload
root_length = Square root of wrapped_length rounded up to a whole integer
Width = root_length divided by 3, rounded down to a whole integer, then plus 1
Height = wrapped_length divided by (Width multiplied by 3), rounded down to a whole integer, then plus 1
```
The `3` here represents how many bytes it takes a Truecolour PNG to store a single pixel (Red + Green + Blue); this means for a given pixel we can store three times more data in the width as we can in the height.
###### Example:
```
wrapped_length = 81
root_length = 9
Width = 4 pixels
   9 / 3 = 3
   3 + 1 = 4 pixels
Height = 7 pixels
   81 / (4 * 3) = 6.75
     -> 81 / 12 = 6.75
   6.75 rounded = 6
   6 + 1 = 7 pixels
```

##### Why these IDHR settings?
 - Bit Depth `8 bits` - This allows each colour channel to be a single byte allowing for simpler reading of the data within the browser
 - Colour Type `2 Truecolour` - This ensures all pixels are a triplet of bytes (Red, Green, Blue) with no alpha transparency. This is important as the alpha layer would need to be hard coded to 100% (0xFF), which takes up more space. By not having transparency it prevents the browser from changing the Red, Green and Blue bytes based on the transparency layer.
 - Compression , FIlter & Interlace `0` - These are all the [PNG standards](https://www.w3.org/TR/2003/REC-PNG-20031110/#11IHDR) defaults

#### IDAT
The IDAT data is written as contiguous "rows" of data; one or multiple. This process continues until all the bytes of the `transport-payload`  have been written
```
+---------------------------------------+-----------------------+
| Filter Byte | Transport Payload Bytes |    Padding Bytes      |
+---------------------------------------+-----------------------+
|     0x00    | First byte_width bytes  |                       |
+---------------------------------------+-----------------------+
|     0x00    | nth byte_width bytes    |                       |
+---------------------------------------+-----------------------+
|     0x00    | Last byte_width bytes   | 0xFF * padding_length |
+---------------------------------------+-----------------------+
```
Using our example from above, this would result in `6 "rows"` with `12 bytes` of `transport-payload` data, plus a final `7th row` with the final `9 bytes` of `transport-payload` data and `3 bytes` of `0xFF` padding (i.e. `0xFF` repeated three times, as three bytes).

##### Byte Width
This is our `Width` multiplied by `3` ; as we can store `3 bytes` of `transport-payload` per pixel width.

##### Padding Length
This is the remaining pixel bytes to fill after we have run out of `transport-payload` bytes. It can be zero bytes long if the `transport-payload` fits perfectly into the rows of bytes.
```
total_capacity = Width multipled by 3 multiplied by Height
wrapped_length = length in bytes of the transport-payload
padding_length = total_capacity minus wrapped_length
```
###### Example :
```
wrapped_length = 81
Width = 4
Height = 7
total_capacity = 84
   4 * 3 * 7 = 84
     12 * 7 = 84
padding_length = 3
   84 - 81 = 3
```

##### Why no PNG filter?
This is to keep the writing of the binary data simple and manipulated; with no filter we can simply write byte for byte -> pixel by pixel

#### IEND
This is just a standard vanilla [IEND Chunk](https://www.w3.org/TR/2003/REC-PNG-20031110/#11IEND)


### Transport Payload
What is this transport payload that you keep hearing about? Well it is some fields of metadata plus the Original Payload (i.e. the protobuf bytes you wish to send).
```
+-------------------------------------------------------------------+
| Version Number | Original-Payload Length | Original Payload Bytes |
+-------------------------------------------------------------------+
```
##### Version Number
This is the number `1` encoded as an [unsigned protobuf varint32](https://protobuf.dev/programming-guides/encoding/#varints) 

##### Original Payload Length
This is the byte length of the `original-payload` encoded as an [unsigned protobuf varint32](https://protobuf.dev/programming-guides/encoding/#varints) 

### Original Payload
This is the output wire bytes of [encoded protobuf 3](https://protobuf.dev/programming-guides/encoding/) data. There is no need to compress or manipulate this data before embedding within the `transport-payload`
