"""
protopng
Allows protobuf to be transported over a PNG
"""
__all__= [
	"create",
	"message","message_field","messages","message_repeated",
	"enum_field","enum_repeated",
	"int32_field","int32_repeated","int64_field","int64_repeated",
	"uint32_field","uint32_repeated","uint64_field","uint64_repeated",
	"sint32_field","sint32_repeated","sint64_field","sint64_repeated",
	"string_field","string_repeated","bytes_field","bytes_repeated",
	"bool_field","bool_repeated",
	"fixed32_field","fixed32_repeated","fixed64_field","fixed64_repeated",
	"sfixed32_field","sfixed32_repeated","sfixed64_field","sfixed64_repeated",
	"float_field","float_repeated","double_field","double_repeated",
	"map_field"
]
__version__="1.0.0"
__version_info__= (1,0,0)
__author__="redorkulated <https://github.com/redorkulated>"

from .protobuf import (
	_varint_enc,
	message,message_field,messages,message_repeated,
	enum_field,enum_repeated,
	int32_field,int32_repeated,int64_field,int64_repeated,
	uint32_field,uint32_repeated,uint64_field,uint64_repeated,
	sint32_field,sint32_repeated,sint64_field,sint64_repeated,
	string_field,string_repeated,bytes_field,bytes_repeated,
	bool_field,bool_repeated,
	fixed32_field,fixed32_repeated,fixed64_field,fixed64_repeated,
	sfixed32_field,sfixed32_repeated,sfixed64_field,sfixed64_repeated,
	float_field,float_repeated,double_field,double_repeated,
	map_field
)
from . import png as _png

PROTOPNG_PROTOCOL_VERSION= 1

def create(original_payload:bytes | bytearray) -> bytes :
	# Create our transport payload
	original_payload_length= len(original_payload)
	transport_payload= (
		# Metadata Payload
		protobuf._varint_enc(PROTOPNG_PROTOCOL_VERSION,is_unsigned=True) # Protopng Protocol Version
		+ protobuf._varint_enc(original_payload_length,is_unsigned=True) # Original Payload Length

		# Append Original Payload
		+ original_payload
	)

	# Wrap payload into a PNG
	return bytes(_png.create(transport_payload))
