import os
import json
import protopng
import randomdata

from enum import Enum

"""
 How to use this
 -----------------
 - Run test.py once to generate these three files
   - test.hex - A hex representation of the protobuf bytes
   - test.json - A JSON representation of the test data
   - test.png - A protopng file containing the protobuf bytes
 - Enter the ExampleNested.proto and test.hex data into https://www.protobufpal.com/ to decode back into JSON
 - Compare this result to the test.json output using https://jsondiff.com/
"""

NUMBER_OF_REPEATED_MESSAGES= 10
OUTPUT_PREFIX="./output/01-ExampleNested"

# Helper functions
byte_print= lambda byte_length : f"{len(byte_length)} bytes ({round(len(byte_length)/1024,2)} kb, {round(len(byte_length)/1024/1024,2)} mb)"
percent_compare= lambda a,b : "100%" if len(b) == 0 else f"{round((len(a) / len(b) * 100)-100,2)}%"

# Create our random data
random_data= randomdata.generate(repeated_message_count=NUMBER_OF_REPEATED_MESSAGES)

# Dump to a JSON file for front end validation
json_bytes= json.dumps(random_data,default=lambda v : v if not isinstance(v,bytes) else list(v),indent=2)
print(f"JSON byte length : {byte_print(json_bytes)}")
with open(OUTPUT_PREFIX+".json","w") as ojson :
	ojson.write(json_bytes)

# Create our protobuf data
pb= protopng.protobuf

# Example of using native Enum as a field
class NativeLetters(Enum) :
	LETTER_UNSPECIFIED= 0
	LETTER_A= 1
	LETTER_B= 2
	LETTER_C= 3
	LETTER_D= 4

Letters= pb.enum_field(NativeLetters)

# Our nested message
ExampleNested= pb.message([
	pb.string_field("exampleStringType",1),
	pb.bytes_field("exampleBytesType",2),
	pb.int32_field("exampleInt32Type",3),
	pb.uint32_field("exampleUInt32Type",4),
	pb.sint32_field("exampleSInt32Type",5),
	pb.int64_field("exampleInt64Type",6),
	pb.uint64_field("exampleUInt64Type",7),
	pb.sint64_field("exampleSInt64Type",8),
	pb.bool_field("exampleBoolType",9),
	pb.fixed32_field("exampleFixed32Type",10),
	pb.fixed64_field("exampleFixed64Type",11),
	pb.sfixed32_field("exampleSFixed32Type",12),
	pb.sfixed64_field("exampleSFixed64Type",13),
	pb.float_field("exampleFloatType",14),
	pb.double_field("exampleDoubleType",15),
	pb.enum_field("exampleEnumType",17,{"LETTER_UNSPECIFIED":0,"LETTER_A":1,"LETTER_B":2,"LETTER_C":3,"LETTER_D":4}),

	pb.string_repeated("exampleRepeatedStringType",21),
	pb.bytes_repeated("exampleRepeatedBytesType",22),
	pb.int32_repeated("exampleRepeatedInt32Type",23),
	pb.uint32_repeated("exampleRepeatedUInt32Type",24),
	pb.sint32_repeated("exampleRepeatedSInt32Type",25),
	pb.int64_repeated("exampleRepeatedInt64Type",26),
	pb.uint64_repeated("exampleRepeatedUInt64Type",27),
	pb.sint64_repeated("exampleRepeatedSInt64Type",28),
	pb.bool_repeated("exampleRepeatedBoolType",29),
	pb.fixed32_repeated("exampleRepeatedFixed32Type",30),
	pb.fixed64_repeated("exampleRepeatedFixed64Type",31),
	pb.sfixed32_repeated("exampleRepeatedSFixed32Type",32),
	pb.sfixed64_repeated("exampleRepeatedSFixed64Type",33),
	pb.float_repeated("exampleRepeatedFloatType",34),
	pb.double_repeated("exampleRepeatedDoubleType",35),
	pb.enum_repeated("exampleRepeatedEnumType",37,Letters),

	pb.string_field("exampleBigFieldID",1337),
])

# Our main message
ExampleTest= pb.message([
	pb.string_field("exampleTestString",1),
	pb.messages("exampleRepeatedMessage",4,[
		pb.string_field("exampleStringType",1),
		pb.bytes_field("exampleBytesType",2),
		pb.int32_field("exampleInt32Type",3),
		pb.uint32_field("exampleUInt32Type",4),
		pb.sint32_field("exampleSInt32Type",5),
		pb.int64_field("exampleInt64Type",6),
		pb.uint64_field("exampleUInt64Type",7),
		pb.sint64_field("exampleSInt64Type",8),
		pb.bool_field("exampleBoolType",9),
		pb.fixed32_field("exampleFixed32Type",10),
		pb.fixed64_field("exampleFixed64Type",11),
		pb.sfixed32_field("exampleSFixed32Type",12),
		pb.sfixed64_field("exampleSFixed64Type",13),
		pb.float_field("exampleFloatType",14),
		pb.double_field("exampleDoubleType",15),
		pb.map_field("exampleMapType",16,(pb.string_field,ExampleNested)),
		pb.enum_field("exampleEnumType",17,NativeLetters),

		pb.string_repeated("exampleRepeatedStringType",21),
		pb.bytes_repeated("exampleRepeatedBytesType",22),
		pb.int32_repeated("exampleRepeatedInt32Type",23),
		pb.uint32_repeated("exampleRepeatedUInt32Type",24),
		pb.sint32_repeated("exampleRepeatedSInt32Type",25),
		pb.int64_repeated("exampleRepeatedInt64Type",26),
		pb.uint64_repeated("exampleRepeatedUInt64Type",27),
		pb.sint64_repeated("exampleRepeatedSInt64Type",28),
		pb.bool_repeated("exampleRepeatedBoolType",29),
		pb.fixed32_repeated("exampleRepeatedFixed32Type",30),
		pb.fixed64_repeated("exampleRepeatedFixed64Type",31),
		pb.sfixed32_repeated("exampleRepeatedSFixed32Type",32),
		pb.sfixed64_repeated("exampleRepeatedSFixed64Type",33),
		pb.float_repeated("exampleRepeatedFloatType",34),
		pb.double_repeated("exampleRepeatedDoubleType",35),
		pb.enum_repeated("exampleRepeatedEnumType",37,NativeLetters),

		pb.message("exampleNestedMessage",42,ExampleNested),

		pb.string_field("exampleBigFieldID",1337),
	])
])

# Encode our random data using our built-in protobuf encoder
# If you are encoding the protobuf using another method (such as SerializeToString)
protobuf_bytes= ExampleTest.encode(random_data)

print(f"Protobuf byte length : {byte_print(protobuf_bytes)}")
print(f" ... {percent_compare(protobuf_bytes,json_bytes)}% compared to the JSON byte length")

# Dump to a HEX dump file for front end validation
with open(OUTPUT_PREFIX+".hex","w") as ohex :
	ohex.write(protobuf_bytes.hex())

# Dump to our PNG file
png_bytes= protopng.create(protobuf_bytes)
print(f"Protopng byte length : {byte_print(png_bytes)}")
print(f" ... {percent_compare(png_bytes,json_bytes)}% compared to the JSON byte length")
print(f" ... {percent_compare(png_bytes,protobuf_bytes)}% compared to the protobuf byte length")
with open(OUTPUT_PREFIX+".png","wb") as opng :
	opng.write(png_bytes)
