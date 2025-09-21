import struct
import zlib
import math
from . import protobuf

_DEFAULT_BIT_DEPTH= 8
_DEFAULT_COLOUR_TYPE= 2
_DEFAULT_FILTER_METHOD= 0
_DEFAULT_FILTER_TYPE= 0
_DEFAULT_INTERLACE= 0
_DEFAULT_COMPRESSION= 0
_PADDING_BYTE= b"\xFF"
_COLOUR_TYPE_PIXEL_WIDTHS= [1,0,3,1,2,0,4]

def calculate_dimensions(payload_length:int) -> tuple[int,int] :
	# We generate the output image to be a rectangle in shape
	# Browsers have been known to not like super wide, one pixel tall, images, this prevents that

	# Get the amount of pixels wide our image will be
	pixel_width= int(
		math.ceil(math.sqrt(payload_length)) // _COLOUR_TYPE_PIXEL_WIDTHS[_DEFAULT_COLOUR_TYPE]
	) + 1

	# Calculate how many bytes we can store per row on the image
	byte_width= pixel_width * _COLOUR_TYPE_PIXEL_WIDTHS[_DEFAULT_COLOUR_TYPE] * (_DEFAULT_BIT_DEPTH // 8)

	# The height is then enough rows to store the payload
	pixel_height= (payload_length // byte_width) + 1

	return pixel_width,pixel_height

def create(payload_bytes:bytes | bytearray) -> bytes :
	pixel_width,pixel_height= calculate_dimensions(len(payload_bytes))
	return bytes(
		IHDR_chunk(pixel_width,pixel_height)
		+ IDAT_chunk(pixel_width,pixel_height,payload_bytes)
		+ IEND_chunk()
	)

def pack_chunk(chunktype:str,data:bytes|bytearray) -> bytes :
	# Pack each chunk according to the PNG specifications
	typeB= chunktype.encode()
	crc32= zlib.crc32(typeB+data)
	crcB= struct.pack("!I",crc32)
	lenB= struct.pack("!I",len(data))
	return lenB + typeB + data + crcB

def IHDR_chunk(pixel_width:int,pixel_height:int,*,bit_depth:int=_DEFAULT_BIT_DEPTH,colour_type:int=_DEFAULT_COLOUR_TYPE,compression:int=_DEFAULT_COMPRESSION,filter_method:int=_DEFAULT_FILTER_METHOD,interlace:int=_DEFAULT_INTERLACE) -> bytes:
	return b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A" + pack_chunk("IHDR",struct.pack("!IIBBBBB",pixel_width,pixel_height,bit_depth,colour_type,compression,filter_method,interlace))

def IDAT_chunk(pixel_width:int,pixel_height:int,payload_data:bytes | bytearray,*,bit_depth:int=_DEFAULT_BIT_DEPTH,colour_type:int=_DEFAULT_COLOUR_TYPE,filter_type:int=_DEFAULT_FILTER_TYPE) -> bytes :
	row_width= pixel_width * _COLOUR_TYPE_PIXEL_WIDTHS[colour_type] * (bit_depth // 8)
	filter_type_byte= struct.pack("!B",filter_type)
	payload_data= bytearray(payload_data)
	return pack_chunk("IDAT",zlib.compress(
		# Each row needs to start with a filter byte
		filter_type_byte

		# Add data, one row at a time
		+ (
			# Put a filter byte between each row
			filter_type_byte.join(
				# Take the number of bytes needed to fill this row
				payload_data[i : i + row_width]
				for i in range(0,len(payload_data),row_width)
			)
		)

		# Add padding bytes (if needed) to fill the remaining pixel data
		+ (_PADDING_BYTE * (row_width - (len(payload_data) % row_width)))
	))

def IEND_chunk() -> bytes:
	return pack_chunk("IEND",b"")
