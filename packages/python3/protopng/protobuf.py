import struct
from enum import EnumType,Enum,IntEnum

_WIRETYPE_VARINT= 0
_WIRETYPE_I64= 1
_WIRETYPE_LEN= 2
_WIRETYPE_I32= 5

def _varint_enc(integer_to_encode : int,*,is_unsigned:bool=False,is_signed:bool=False,is_integer:bool=False,is_wide:bool=False) -> bytearray :
	encoded_bytes= bytearray()

	# Unsigned Integer (uint64)
	if is_unsigned or (not is_signed and not is_integer) :
		is_unsigned= True
		if integer_to_encode < 0 : raise ValueError("Trying to push a negative number into an unsigned int")

	# Normal Integer (int32/int64)
	# Two's compliment encoding
	elif is_integer and integer_to_encode < 0 and is_wide : integer_to_encode+= (1 << 64)
	elif is_integer and integer_to_encode < 0 : integer_to_encode+= (1 << 32)

	# Signed Integer (sint32/sint64)
	# Apply zig-zag encoding
	elif is_signed and is_wide : integer_to_encode= (integer_to_encode << 1) ^ (integer_to_encode >> 63)
	elif is_signed : integer_to_encode= (integer_to_encode << 1) ^ (integer_to_encode >> 31)

	# Ensure we do not have a negative number before we go into the loop
	if integer_to_encode < 0 : raise ValueError("Wrong type used as number provided is negative")

	# Pack into bytes
	next_byte= integer_to_encode & 0x7f
	integer_to_encode>>= 7
	while integer_to_encode :
		encoded_bytes.append(next_byte|0x80)
		next_byte= integer_to_encode & 0x7f
		integer_to_encode >>= 7
	encoded_bytes.append(next_byte)

	return encoded_bytes

def _varints_enc(integers_to_encode:list[int] | tuple[int],*,is_unsigned:bool=False,is_signed:bool=False,is_integer:bool=False,is_wide:bool=False) -> bytearray :
	encoded_bytes= bytearray()
	# Convert each integer into bytes and add it to the output encoded bytes
	for integer_to_encode in integers_to_encode :
		encoded_bytes+= _varint_enc(integer_to_encode,is_unsigned=is_unsigned,is_signed=is_signed,is_integer=is_integer,is_wide=is_wide)
	return encoded_bytes

def _enclen(length:int|bytearray|bytes|list|tuple|str ,/) -> bytearray:
	return _varint_enc(len(length) if isinstance(length,(bytearray,bytes,list,tuple,str,)) else length,is_unsigned=True)

def _tag(typ:int,field:int,/) -> bytearray:
	return _varint_enc((field << 3) | typ,is_unsigned=True)

def _empty(field:int=0) -> bytearray:
	return bytearray()

class _field(object) :
	_packed= True
	_repeated= False
	_wire_type= None

	def __init__(self,field_name:str,field_number:int,/) :
		# Sanity check input
		if (
			field_name is None or not isinstance(field_name,str)
			or field_number is None or not isinstance(field_number,int) or field_number <= 0
		) :
			raise TypeError(f"protopng.protobuf.{type(self).__name__} provided parameters of the wrong type")
		self.field_name= field_name
		self.field_number= field_number

	def _wire(self,encoded_bytes:bytes|bytearray|list|tuple,force_repeated:bool=False) :
		# Packed repeated items
		if (self._repeated or force_repeated) and self._packed :
			if isinstance(encoded_bytes,(list,tuple)) :
				encoded_bytes= b"".join(encoded_bytes)
			return _tag(_WIRETYPE_LEN,self.field_number) + _enclen(encoded_bytes) + encoded_bytes

		# Non-Packed repeated items
		elif self._repeated or force_repeated :
			if not isinstance(encoded_bytes,(list,tuple)) :
				encoded_bytes= (encoded_bytes,)
			return b"".join(_tag(_WIRETYPE_LEN,self.field_number) + _enclen(eb) + eb for eb in encoded_bytes)

		# Normal length items
		elif self._wire_type == _WIRETYPE_LEN :
			return _tag(self._wire_type,self.field_number) + _enclen(encoded_bytes) + encoded_bytes

		# Everything else
		return _tag(self._wire_type,self.field_number) + encoded_bytes

	def check_type_is_none(self,value_to_encode:int|float|bytes|str|list|tuple|None,types:tuple) :
		if value_to_encode is None :
			return True

		if not isinstance(value_to_encode,types) :
			raise TypeError(f"""protopng.protobuf.messages.{type(self).__name__} was expecting "{', '.join(t.__name__ for t in types)}"; "{type(value_to_encode).__name__}" provided instead""")

		return False

class _field_repeated(_field) :
	_repeated= True
	_rtype_instance= None
	def encode(self,value_to_encode:None|list|tuple,/) -> bytearray :
		# Return nothing if empty
		if value_to_encode is None :
			return _empty()

		# Check this is actually a repeated value
		if not isinstance(value_to_encode,(list|tuple)) :
			raise TypeError(f"protopng.protobuf.messages.{type(self).__name__} was expecting a list or tuple; {type(value_to_encode).__name__} provided instead")

		# Get an instance of the non-repeated type ready for us to use
		if self._rtype_instance is None :
			self._rtype_instance= (
				self._repeated_type(self.field_name,self.field_number,self) if self._repeated_type is message
				else self._repeated_type(self.field_name,self.field_number,self) if self._repeated_type is enum_field
				else self._repeated_type(self.field_name,self.field_number)
			)

		return [self._rtype_instance.encode(v) for v in value_to_encode]

class message(_field) :
	_wire_type= _WIRETYPE_LEN
	_packed= False

	def __init__(self,field_name:list|tuple|str,field_number:int|None=None,fields:_field|None|list|tuple=None,/) :
		# Just fields in an array
		# - (<Fields>)
		# This method is used when defining a Message without linking it to a field
		if field_name is not None and isinstance(field_name,(list,tuple)) :
			fields= field_name
			field_name= None
			field_number= None

		# We have an array of fields as the last parameter
		# - (<Field Name>, <Field Number>, <Fields>)
		elif (
			field_name is not None and isinstance(field_name,str)
			and field_number is not None and isinstance(field_number,int) and field_number > 0
			and fields is not None and isinstance(fields,(list,tuple))
		) :
			pass

		# We have a message as the last parameter
		# - (<Field Name>, <Field Number>, <Message()>)
		elif (
			field_name is not None and isinstance(field_name,str)
			and field_number is not None and isinstance(field_number,int) and field_number > 0
			and fields is not None and isinstance(fields,(message,messages))
		) :
			fields= fields.fields.values()

		# Unknown usage
		else :
			raise TypeError("protopng.protobuf.message provided incorrect parameters")

		# Go through fields and create an output
		self.fields= {x.field_name : x for x in fields if isinstance(x,_field) and x.field_name is not None and x.field_number is not None}
		self.field_name= field_name
		self.field_number= field_number

	def encode(self,value_to_encode:None|dict,/) -> bytearray :
		# Go through the input and create an output
		if self.check_type_is_none(value_to_encode,(dict,)) : return _empty()
		return b"".join(self.fields[x]._wire(self.fields[x].encode(value_to_encode[x])) for x in self.fields if x in value_to_encode and value_to_encode[x] is not None)
message_field= message

class messages(_field_repeated) :
	_repeated_type= message
	_packed= message._packed
	def __init__(self,field_name:str,field_number:int,fields:message|list|tuple,/):
		# Attempt to create message with these parameters
		single_message= message(field_name,field_number,fields)

		# Check this is not a fieldless message definition
		if single_message.field_number is None :
			raise TypeError("protopng.protobuf.messages provided incorrect parameters")

		# Assign these to ourself
		self.fields= single_message.fields
		self.field_name= single_message.field_name
		self.field_number= single_message.field_number
message_repeated= messages

class enum_field(_field) :
	_wire_type= _WIRETYPE_VARINT
	_packed= True
	def __init__(self,field_name:dict|Enum|IntEnum|list|tuple|str,field_number:int|None=None,fields:_field|dict|Enum|IntEnum|list|tuple=None,/) :
		# Just fields in a dict, native enum or list-of-pairs
		# - (<Values>)
		# This method is used when defining an enum without linking it to a field
		if field_name is not None and isinstance(field_name,(dict,EnumType,list,tuple,enum_field)) :
			fields= field_name
			field_name= None
			field_number= None

		# We have fields as a dict, native enum or list-of-pairs as the last parameter
		# - (<Field Name>, <Field Number>, <Values>)
		elif (
			field_name is not None and isinstance(field_name,str)
			and field_number is not None and isinstance(field_number,int) and field_number > 0
			and fields is not None and isinstance(fields,(dict,EnumType,list,tuple,enum_field,enum_repeated))
		) :
			pass

		# Unknown usage
		else :
			raise TypeError("protopng.protobuf.enum_field provided incorrect parameters")

		# Go through fields and create an output
		if isinstance(fields,dict) : self.fields= {k : v for k,v in fields.items() if isinstance(k,str) and isinstance(v,int)}
		elif isinstance(fields,(enum_field,enum_repeated)) : self.fields= fields.fields
		elif isinstance(fields,EnumType) : self.fields= {v.name : v.value for v in fields if isinstance(v.name,str) and isinstance(v.value,int)}
		elif isinstance(fields,(list,tuple)) : self.fields= {k : v for k,v in fields if isinstance(k,str) and isinstance(v,int)}
		else : raise TypeError("protopng.protobuf.enum_field provided incorrect parameters")
		self.fields|= {v : v for v in self.fields.values()}

		self.field_name= field_name
		self.field_number= field_number

	def encode(self,value_to_encode:None|str|int,/) -> bytearray :
		# Find the matching integer value and send that over the wire
		# If there is matching entry then just send the integer as is
		if value_to_encode is not None and isinstance(value_to_encode,(Enum,IntEnum)) :
			value_to_encode= value_to_encode.value
		if self.check_type_is_none(value_to_encode,(int,str)) : return _empty()
		return _varint_enc(self.fields.get(value_to_encode,value_to_encode),is_integer=True)

class enum_repeated(_field_repeated) :
	_repeated_type= enum_field
	_packed= enum_field._packed
	def __init__(self,field_name:str,field_number:int,fields:enum_field|dict|Enum|list|tuple,/) :
		# Attempt to create enum with these parameters
		single_enum= enum_field(field_name,field_number,fields)

		# Check this is not a fieldless enum definition
		if single_enum.field_number is None :
			raise TypeError("protopng.protobuf.enum_repeated provided incorrect parameters")

		# Assign these to ourself
		self.fields= single_enum.fields
		self.field_name= single_enum.field_name
		self.field_number= single_enum.field_number

class _varint_field(_field) :
	_wire_type= _WIRETYPE_VARINT
	_packed= True
	_is_signed= False
	_is_unsigned= False
	_is_integer= False
	_is_wide= False
	def encode(self,value_to_encode:None|int,/) -> bytearray :
		if self.check_type_is_none(value_to_encode,(int,)) : return _empty()
		return _varint_enc(value_to_encode,is_signed=self._is_signed,is_unsigned=self._is_unsigned,is_integer=self._is_integer,is_wide=self._is_wide)

class _varint_repeated(_field_repeated) :
	_packed= _varint_field._packed

class int32_field(_varint_field) :
	_is_integer= True

class int32_repeated(_varint_repeated) :
	_repeated_type= int32_field

class int64_field(_varint_field) :
	_is_integer= True
	_is_wide= True

class int64_repeated(_varint_repeated) :
	_repeated_type= int64_field
	_is_wide= True

class uint32_field(_varint_field) :
	_is_unsigned= True

class uint32_repeated(_varint_repeated) :
	_repeated_type= uint32_field

class uint64_field(_varint_field) :
	_is_unsigned= True
	_is_wide= True

class uint64_repeated(_varint_repeated) :
	_repeated_type= uint64_field
	_is_wide= True

class sint32_field(_varint_field) :
	_is_signed= True

class sint32_repeated(_varint_repeated) :
	_repeated_type= sint32_field

class sint64_field(_varint_field) :
	_is_signed= True
	_is_wide= True

class sint64_repeated(_varint_repeated) :
	_repeated_type= sint64_field
	_is_wide= True

class string_field(_field) :
	_wire_type= _WIRETYPE_LEN
	_packed= False
	def encode(self,value_to_encode:None|str,/) -> bytearray|bytes :
		if self.check_type_is_none(value_to_encode,(str,)) : return _empty()
		return value_to_encode.encode()

class string_repeated(_field_repeated) :
	_repeated_type= string_field
	_packed= string_field._packed

class bytes_field(_field) :
	_wire_type= _WIRETYPE_LEN
	_packed= False
	def encode(self,value_to_encode:None|bytes|bytearray,/) -> bytearray|bytes :
		if self.check_type_is_none(value_to_encode,(bytes,bytearray)) : return _empty()
		return value_to_encode

class bytes_repeated(_field_repeated) :
	_repeated_type= bytes_field
	_packed= bytes_field._packed

class bool_field(_field) :
	_wire_type= _WIRETYPE_VARINT
	_packed= True
	def encode(self,value_to_encode:None|bool,/) -> bytearray :
		if self.check_type_is_none(value_to_encode,(bool,)) : return _empty()
		return bytearray((1 if value_to_encode else 0,))

class bool_repeated(_field_repeated) :
	_repeated_type= bool_field
	_packed= bool_field._packed

class _buffer_field(_field) :
	_packed= True
	def encode(self,value_to_encode:None|float|int,/) -> bytearray|bytes :
		if self.check_type_is_none(value_to_encode,self._allowed_types) : return _empty()
		return struct.pack(self._struct_pack,value_to_encode)

class _buffer_repeated(_field_repeated) :
	_packed= _buffer_field._packed

class fixed32_field(_buffer_field) :
	_wire_type= _WIRETYPE_I32
	_allowed_types= (int,)
	_struct_pack="<I"

class fixed32_repeated(_buffer_repeated) :
	_repeated_type= fixed32_field

class fixed64_field(_buffer_field) :
	_wire_type= _WIRETYPE_I64
	_allowed_types= (int,)
	_struct_pack="<Q"

class fixed64_repeated(_buffer_repeated) :
	_repeated_type= fixed64_field

class sfixed32_field(_buffer_field) :
	_wire_type= _WIRETYPE_I32
	_allowed_types= (int,)
	_struct_pack="<i"

class sfixed32_repeated(_buffer_repeated) :
	_repeated_type= sfixed32_field

class sfixed64_field(_buffer_field) :
	_wire_type= _WIRETYPE_I64
	_allowed_types= (int,)
	_struct_pack="<q"

class sfixed64_repeated(_buffer_repeated) :
	_repeated_type= sfixed64_field

class float_field(_buffer_field) :
	_wire_type= _WIRETYPE_I32
	_allowed_types= (float,int)
	_struct_pack="<f"

class float_repeated(_buffer_repeated) :
	_repeated_type= float_field

class double_field(_buffer_field) :
	_wire_type= _WIRETYPE_I64
	_allowed_types= (float,int)
	_struct_pack="<d"

class double_repeated(_buffer_repeated) :
	_repeated_type= double_field

class map_field(_field) :
	_wire_type= message._wire_type
	_packed= message._packed
	_repeated= True
	_repeated_type= message

	def __init__(self,field_name:str,field_number:int,key_value_types:tuple|list,/) :
		# Do the usual field stuff
		super().__init__(field_name,field_number)

		# Check types
		if not (
			key_value_types[0] == string_field or key_value_types[0] == bool_field
			or key_value_types[0] == int32_field or key_value_types[0] == int64_field
			or key_value_types[0] == uint32_field or key_value_types[0] == uint64_field
			or key_value_types[0] == sint32_field or key_value_types[0] == sint64_field
			or key_value_types[0] == fixed32_field or key_value_types[0] == sfixed32_field
			or key_value_types[0] == fixed64_field or key_value_types[0] == sfixed64_field
		) :
			raise TypeError("Map key type can only be one of string_field, int32_field, int64_field, uint32_field, uint64_field, sint32_field, sint64_field, fixed32_field, sfixed32_field, fixed64_field, sfixed32_field or bool_field")

		if not (
			key_value_types[1] == string_field or key_value_types[1] == bool_field or key_value_types[1] == bytes_field
			or key_value_types[1] == int32_field or key_value_types[1] == int64_field
			or key_value_types[1] == uint32_field or key_value_types[1] == uint64_field
			or key_value_types[1] == sint32_field or key_value_types[1] == sint64_field
			or key_value_types[1] == fixed32_field or key_value_types[1] == sfixed32_field
			or key_value_types[1] == fixed64_field or key_value_types[1] == sfixed64_field
			or key_value_types[1] == float_field or key_value_types[1] == double_field
			or key_value_types[1] == enum_field
			or isinstance(key_value_types[1],message)
		) :
			raise TypeError("Map value type must be a non-repeated field or a non-repeated message")

		# Setup our internal message structure to support encoding later
		self._internal_message= message([
			key_value_types[0]("k",1),
			message("v",2,key_value_types[1]) if isinstance(key_value_types[1],message) else key_value_types[1]("v",2)
		])

	def encode(self,value_to_encode:None|dict,/) -> bytearray :
		# Encode this as multiple messages with our k:1,v:2 structure 
		if self.check_type_is_none(value_to_encode,(dict,)) : return _empty()
		return [self._internal_message.encode({"k":k,"v":v}) for k,v in value_to_encode.items()]
