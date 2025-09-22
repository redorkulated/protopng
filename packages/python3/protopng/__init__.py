"""
protopng
Allows protobuf to be transported over a PNG
"""
__all__= ["create","protobuf"]
__version__="1.0.0"
__version_info__= (1,0,0)
__author__="redorkulated <https://github.com/redorkulated>"

from . import protobuf
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
