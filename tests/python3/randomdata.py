# Here we will generate random data on demand that matches our example proto format
# ./tests/protobuf/01-ExampleNested.proto

import random

REPEATED_MESSAGE_COUNT= 10
REPEATED_ITEM_MAX_COUNT= 5
OPTIONAL_RAND_PERCENT_CHANCE= 33 # 1 to 100

STRING_LENGTH_MAX_COUNT= 20
BYTES_LENGTH_MAX_COUNT= 20
UINTEGER32_MAX= 99999999
UINTEGER32_MIN= 0
SINTEGER32_MAX= 99999999
SINTEGER32_MIN= SINTEGER32_MAX * -1
UINTEGER64_MAX= 0xFFFFFFFFFFFFFFFF
UINTEGER64_MIN= 0
SINTEGER64_MAX= 0x7FFFFFFFFFFFFFFF
SINTEGER64_MIN= -0x8000000000000000

FIXED32_MAX= 0xFFFFFFFF
FIXED32_MIN= 0
SFIXED32_MAX= 0x7FFFFFF
SFIXED32_MIN= SFIXED32_MAX * -1

FIXED64_MAX= 0xFFFFFFFFFFFFFFFF
FIXED64_MIN= 0
SFIXED64_MAX= 0x7FFFFFFFFFFFFFFF
SFIXED64_MIN= SFIXED64_MAX * -1

FLOAT_MAX= 100
FLOAT_MIN= FLOAT_MAX * -1
DOUBLE_MAX= FLOAT_MAX
DOUBLE_MIN= FLOAT_MIN

ENUM_VALUES= ["LETTER_UNSPECIFIED","LETTER_A","LETTER_B","LETTER_C","LETTER_D"]

REMOVE_NONE_VALUES= True

def generate(repeated_message_count=REPEATED_MESSAGE_COUNT) :
	return remove_none_values({
		"exampleTestString":generate_type_string(),
		"exampleRepeatedMessage":generate_repeated(generate_message_ExampleRepeated,minimum=repeated_message_count,maximum=repeated_message_count)
	})

def generate_optional(type_generator,*,random_chance=OPTIONAL_RAND_PERCENT_CHANCE) :
	if random.randint(1,100) <= random_chance : return None
	return type_generator()

def generate_repeated(type_generator,*,minimum=0,maximum=REPEATED_ITEM_MAX_COUNT) :
	if minimum != maximum : maximum= random.randint(minimum,maximum)
	return [type_generator() for i in range(0,maximum)]

def remove_none_values(original_dict) :
	if not REMOVE_NONE_VALUES : return original_dict
	return {k : original_dict[k] for k,v in original_dict.items() if v is not None}

def generate_message_ExampleRepeated() :
	return remove_none_values({
		"exampleStringType":generate_optional(generate_type_string),
		"exampleBytesType":generate_optional(generate_type_bytes),
		"exampleInt32Type":generate_optional(generate_type_int32),
		"exampleUInt32Type":generate_optional(generate_type_uint32),
		"exampleSInt32Type":generate_optional(generate_type_sint32),
		"exampleInt64Type":generate_optional(generate_type_int64),
		"exampleUInt64Type":generate_optional(generate_type_uint64),
		"exampleSInt64Type":generate_optional(generate_type_sint64),
		"exampleBoolType":generate_optional(generate_type_bool),
		"exampleFixed32Type":generate_optional(generate_type_fixed32),
		"exampleFixed64Type":generate_optional(generate_type_fixed64),
		"exampleSFixed32Type":generate_optional(generate_type_sfixed32),
		"exampleSFixed64Type":generate_optional(generate_type_sfixed64),
		"exampleFloatType":generate_optional(generate_type_float),
		"exampleDoubleType":generate_optional(generate_type_double),
		"exampleMapType":generate_optional(generate_type_map),
		"exampleEnumType":generate_optional(generate_type_enum),

		"exampleRepeatedStringType":generate_repeated(generate_type_string),
		"exampleRepeatedBytesType":generate_repeated(generate_type_bytes),
		"exampleRepeatedInt32Type":generate_repeated(generate_type_int32),
		"exampleRepeatedUInt32Type":generate_repeated(generate_type_uint32),
		"exampleRepeatedSInt32Type":generate_repeated(generate_type_sint32),
		"exampleRepeatedInt64Type":generate_repeated(generate_type_int64),
		"exampleRepeatedUInt64Type":generate_repeated(generate_type_uint64),
		"exampleRepeatedSInt64Type":generate_repeated(generate_type_sint64),
		"exampleRepeatedBoolType":generate_repeated(generate_type_bool),
		"exampleRepeatedFixed32Type":generate_repeated(generate_type_fixed32),
		"exampleRepeatedFixed64Type":generate_repeated(generate_type_fixed64),
		"exampleRepeatedSFixed32Type":generate_repeated(generate_type_sfixed32),
		"exampleRepeatedSFixed64Type":generate_repeated(generate_type_sfixed64),
		"exampleRepeatedFloatType":generate_repeated(generate_type_float),
		"exampleRepeatedDoubleType":generate_repeated(generate_type_double),
		"exampleRepeatedEnumType":generate_repeated(generate_type_enum),

		"exampleNestedMessage":generate_optional(generate_message_ExampleNested),

		"exampleBigFieldID":generate_optional(generate_type_string),
	})

def generate_message_ExampleNested() :
	return remove_none_values({
		"exampleStringType":generate_optional(generate_type_string),
		"exampleBytesType":generate_optional(generate_type_bytes),
		"exampleInt32Type":generate_optional(generate_type_int32),
		"exampleUInt32Type":generate_optional(generate_type_uint32),
		"exampleSInt32Type":generate_optional(generate_type_sint32),
		"exampleInt64Type":generate_optional(generate_type_int64),
		"exampleUInt64Type":generate_optional(generate_type_uint64),
		"exampleSInt64Type":generate_optional(generate_type_sint64),
		"exampleBoolType":generate_optional(generate_type_bool),
		"exampleFixed32Type":generate_optional(generate_type_fixed32),
		"exampleFixed64Type":generate_optional(generate_type_fixed64),
		"exampleSFixed32Type":generate_optional(generate_type_sfixed32),
		"exampleSFixed64Type":generate_optional(generate_type_sfixed64),
		"exampleFloatType":generate_optional(generate_type_float),
		"exampleDoubleType":generate_optional(generate_type_double),
		"exampleEnumType":generate_optional(generate_type_enum),

		"exampleRepeatedStringType":generate_repeated(generate_type_string),
		"exampleRepeatedBytesType":generate_repeated(generate_type_bytes),
		"exampleRepeatedInt32Type":generate_repeated(generate_type_int32),
		"exampleRepeatedUInt32Type":generate_repeated(generate_type_uint32),
		"exampleRepeatedSInt32Type":generate_repeated(generate_type_sint32),
		"exampleRepeatedInt64Type":generate_repeated(generate_type_int64),
		"exampleRepeatedUInt64Type":generate_repeated(generate_type_uint64),
		"exampleRepeatedSInt64Type":generate_repeated(generate_type_sint64),
		"exampleRepeatedBoolType":generate_repeated(generate_type_bool),
		"exampleRepeatedFixed32Type":generate_repeated(generate_type_fixed32),
		"exampleRepeatedFixed64Type":generate_repeated(generate_type_fixed64),
		"exampleRepeatedSFixed32Type":generate_repeated(generate_type_sfixed32),
		"exampleRepeatedSFixed64Type":generate_repeated(generate_type_sfixed64),
		"exampleRepeatedFloatType":generate_repeated(generate_type_float),
		"exampleRepeatedDoubleType":generate_repeated(generate_type_double),
		"exampleRepeatedEnumType":generate_repeated(generate_type_enum),

		"exampleBigFieldID":generate_optional(generate_type_string),
	})

def generate_type_string():
	return "".join(
		chr(
				(0x100 + b) if b < 0x32 # Control chars, convert into Latin Extended-A
			else 0x20A4 if b == 0x7F # Control char, convert into pound sign
			else (0x100 + b) if b >= 0x80 and b < 0xA1 # Control chars, convert into Latin Extended-B
			else 0x221E if b == 0xAD # Shy non-printable, convert into infinity
			else b
		)
		for b in random.randbytes(random.randint(1,BYTES_LENGTH_MAX_COUNT))
	)

def generate_type_bytes():
	return random.randbytes(random.randint(1,BYTES_LENGTH_MAX_COUNT))

def generate_type_int32():
	return random.randint(SINTEGER32_MIN,SINTEGER32_MAX)

def generate_type_uint32():
	return random.randint(UINTEGER32_MIN,UINTEGER32_MAX)

def generate_type_sint32():
	return random.randint(SINTEGER32_MIN,SINTEGER32_MAX)

def generate_type_int64():
	return random.randint(SINTEGER64_MIN,SINTEGER64_MAX)

def generate_type_uint64():
	return random.randint(UINTEGER64_MIN,UINTEGER64_MAX)

def generate_type_sint64():
	return random.randint(SINTEGER64_MIN,SINTEGER64_MAX)

def generate_type_bool():
	return random.choice((True,False))

def generate_type_fixed32():
	return random.randint(FIXED32_MIN,FIXED32_MAX)

def generate_type_fixed64():
	return random.randint(FIXED64_MIN,FIXED64_MAX)

def generate_type_sfixed32():
	return random.randint(SFIXED32_MIN,SFIXED32_MAX)

def generate_type_sfixed64():
	return random.randint(SFIXED64_MIN,SFIXED64_MAX)

def generate_type_float():
	return round(random.uniform(FLOAT_MIN,FLOAT_MAX),6)

def generate_type_double():
	return round(random.uniform(DOUBLE_MIN,DOUBLE_MAX),15)

def generate_type_map() :
	return {generate_type_string() : x for x in generate_repeated(generate_message_ExampleNested,maximum=3)}

def generate_type_enum():
	return random.choice(ENUM_VALUES)


