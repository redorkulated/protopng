
# Python protopng module

## Installation
The module requires just the files located within the [./protopng](./protopng) directory. Therefore you can take a copy of this directory and use it directly as an import:
```
import protopng
```
By design there are no requirements needed to be installed for this module to work; only the [python built-in modules](https://docs.python.org/3/py-modindex.html) are needed.

## Example
A very simple example of how to use the protopng python module
```
import protopng
# Generate the encoded protobuf data using the standard compiled protobuf interface
protobuf_bytes= ExampleProtobuf.SerializeToString()

# Create our protopng
png_bytes= protopng.create(protobuf_bytes)

# Use the output however we need
with open("ExampleProtobuf.png","wb") as output_png :
	output_png.write(png_bytes)
```
For a more in-depth example have a look at the [tests here](../../tests/python3) .
For more detail on the protopng encoding itself [see the protocol here](../../protocol/protocol-v1.md) .

## Interface

### Creating the protopng
The interface is super simple if you are already using the standard [protobuf serialisation](https://protobuf.dev/getting-started/pythontutorial/). 

##### Create
`protopng.create`(

> `original_payload` - `<bytes>` - The original protobuf encoded payload

) -> returns `bytes`

That's it, you can now return these bytes over HTTP or safe them to a .png file.


# Protobuf Encoding
You can either use the official and supported [python protobuf](https://protobuf.dev/getting-started/pythontutorial/) encoder or use the on-the-fly encoder packaged with this python module. Either method will output [fully compatible](https://protobuf.dev/programming-guides/encoding/) protobuf binary data that can be packaged into a protopng.

## On-the-fly Encoding

Here we will go into the details for the interface packaged with this module. For a full example you can checkout the test [01-ExampleNested.py](../../tests/python3/01-ExampleNested.py) .

To access this interface it is all within `protopng.protobuf` .

### Message
At the heart of protopng, much the same as protobuf itself is the message. This method can be used in two ways, once to define a message (we will cover that in this section) and secondly as a field in another message ([see fields](#user-content-complex-fields)).

##### Defining a Message
A message is defined as a list of fields

`protopng.protobuf.message`(

> `fields` - `<[field]>` - A `list`/`tuple` of fields

) -> returns `protopng.protobuf.message` instance

##### Encoding Data using the Message
The `encode` method of a message instance can be used :

message`.encode`(

> `data` - `<dict>` - A dict of data that is matching the protobuf specification defined for this message

) -> returns `bytes` protobuf encoded data

##### Encoding Example
```
ExampleMessage= protopng.protobuf.message([
	protopng.protobuf.string_field("exampleStringType" , 1),
])
encoded_bytes= ExampleMessage.encode({"exampleStringType":"Hello, World!"})
```

##### Nesting Messages
You can [nest](https://protobuf.dev/programming-guides/proto3/#nested) messages within each other. Here is a very simple example
```
MessageA= protopng.protobuf.message([
	protopng.protobuf.string_field("exampleStringType" , 1),
])
MessageB= protopng.protobuf.message([
	protopng.protobuf.message("nestedA" , 1 , MessageB),
	protopng.protobuf.messages("nestedARepeated" , 2 , MessageB),
])
```

### Enumerations (Enums)
A basic Enum is following the same pattern as within [protobuf](https://protobuf.dev/programming-guides/proto3/#enum); this is that you have values (a string) and constants (a number). This method can be used in two ways, once to define an enum (we will cover that in this section) and secondly as a field in a message [(see fields)](#user-content-complex-fields). 

##### Defining an Enum
An Enum is defined as a a list of values and constants

`protopng.protobuf.enum_field`(

> `values` - `<dict>` or `<list>` or `<Enum>` - The list of values and constants within this Enum

) -> returns `protobuf.enum_field` object

List as an input expects:
`[ [ value <string> , constant <number> ] , ....]`
Dict as an input expects:
`{ value <string> : constant <number> , ....}`
Enum as an input expects
`Enum` Class

##### Examples
Defining an Enum using a `Dict` as input:
```
Example= protopng.protobuf.enum_field({
	"EXAMPLE_UNSPECIFIED":0,
	"EXAMPLE_A":1
})
```

Defining an Enum using an `list of lists` as input
```
Example= protopng.protobuf.enum_field([
	["EXAMPLE_UNSPECIFIED" , 0],
	["EXAMPLE_A" , 1]
])
```

Defining an Enum using an `Enum` as input
```
from enum import Enum
class ExampleEnum(Enum) :
	EXAMPLE_UNSPECIFIED= 0
	EXAMPLE_A= 1
Example= protopng.protobuf.enum_field(ExampleEnum)
```

### Fields
Protopng allows you to define the fields within messages to match any type that [protobuf has](https://protobuf.dev/programming-guides/proto3/#specifying-types). There is no way to define fields as optional since we treat all fields as optional. You can, and should, define a field as repeated, for each type there exists a singleton method and repeated method.

#### Simple Fields
`protopng.protobuf.<method>`(

> `field_name` - `string` - The name and key of this field

> `field_number` - `int` - The integer number of this field

)

| Protobuf Type | Single Method  |  Repeated Method  | Expected Type [1] |
----------------|----------------|-------------------|-------------------|
| double        | double_field   | double_repeated   | int, float        |
| float         | float_field    | float_repeated    | int, float        |
| int32         | int32_field    | int32_repeated    | int               |
| int64         | int64_field    | int64_repeated    | int               |
| uint32        | uint32_field   | uint32_repeated   | int               |   
| uint64        | uint64_field   | uint64_repeated   | int               |
| sint32        | sint32_field   | sint32_repeated   | int               |
| sint64        | sint64_field   | sint64_repeated   | int               |
| fixed32       | fixed32_field  | fixed32_repeated  | int               |
| fixed64       | fixed64_field  | fixed64_repeated  | int               |
| sfixed32      | sfixed32_field | sfixed32_repeated | int               |
| sfixed64      | sfixed64_field | sfixed64_repeated | int               |
| bool          | bool_field     | bool_repeated     | bool              |
| string        | string_field   | string_repeated   | str               |
| bytes         | bytes_field    | bytes_repeated    | bytes             |

- [1] A repeated field expects an iterator returning this type

##### Simple Fields Example
```
MessageWithSimpleFields= protopng.protobuf.message([
	protopng.protobuf.string_field("exampleString" , 1),
	protopng.protobuf.float_field("exampleFloat" , 2),
	protopng.protobuf.bool_repeated("repeatedBooleans" , 3),
])
```

#### Complex Fields
These field types require a third parameter as part of it's definition
`protopng.rotobuf.<method>`(

> `field_name` - `str` - The name and key of this field

> `field_number` - `int` - The integer number of this field

> `additional_parameter` - `mixed` - Additional information needed to define this field

)
| Protobuf Type | Single Method  |  Repeated Method  | Expected Type [1] | Additional Parameter |
----------------|----------------|-------------------|----------------------|----------------------|
| map           | map_field      | N/A [2]           | Dict               | list [`key type` , `value type`] [3] |
| message       | message        | messages          | Dict               | `message` instance or a `list of fields` [4] |
| enum          | enum_field     | enum_repeated     | Enum,Int,Str      | Defined `enum_field` instance, `value/constant dict` [6], a `list of values/constants` [7] or an `Enum` class [8]

- [1] A repeated field expects a iterator returning this type
- [2] Map's can not be repeated in protobuf
- [3] Key type is one of `string_field`, `int32_field`, `int64_field`, `uint32_field`, `uint64_field`, `sint32_field`, `sint64_field`, `fixed32_field`, `sfixed32_field`, `fixed64_field`, `sfixed32_field` or `bool_field` . Value type can be any non-repeated type (excluding `map_field`).
- [4] See [defining a message](#defining-a-message) above for how to structure this list
- [5] The enum string value is returned. Unknown enum constants received will be cast to a string and also returned; this is following the [open enum](https://protobuf.dev/programming-guides/enum/) process
- [6] See [defining an enum](#defining-an-enum) above for how to structure this dict
- [7] See [defining an enum](#defining-an-enum) above for how to structure this list
- [7] See [defining an enum](#defining-an-enum) above for how to structure this Enum

##### Map Field Example
You need to define the key type and value type of the items within the map. Protobuf does not allow multiple types as a value but does allow the value to be a message (where optional fields can be used).
```
ExampleMessageWithMap= protopng.protobuf.message([
	protopng.map_field("mapWithSimpleType" , 1 , [ protopng.protobuf.string_field , protopng.protobuf.uint32_field ] ),
	protopng.map_field("mapWithMessage" , 2 , [ protopng.protobuf.string_field , AnotherDefinedMessage ] ),
])
```

## Handling of None Fields
Any value provided as `None` fails safe and is silently ignored and not sent over the wire. It is your responsibility to know if this field should be optional or not.
