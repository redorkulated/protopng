# Javascript protopng module

## Installation
The module requires just the files located within the [./protopng](./protopng) directory. Therefore you can take a copy of this directory and use it directly as an import:
```
import * as protopng from "./protopng/protopng.js"
```

## Example
A very simple example of how to use the protopng javascript module
```
import * as protopng from "./protopng/protopng.js"
const ExampleMessage= protopng.message([
	protopng.string_field("exampleStringType" , 1),
]);
ExampleTest.fetch("./example.png")
  .then((fetched_data)=>{ console.log(fetched_data); }
  .catch((process_error)=>console.error(process_error); }
```
For a more in-depth example have a look at the [tests here](../../tests/javascript) .

## Interface

### Message
At the heart of protopng, much the same as protobuf itself is the message. This method can be used in two ways, once to define a message (we will cover that in this section) and secondly as a field in another message [(see fields)](#user-content-complex-fields).

##### Defining a Message
A message is defined as a list of fields

`protopng.message`(

> `fields` - `<[field]>` - An array of fields

) -> returns `protopng.message` object

##### Fetching Data using the Message
Once a message is constructed it's `fetch` method can be used :

message`.fetch`(
> `path` - `<string>` - The URL of the protopng encoded PNG, this can either be a static PNG or returned via an API. The `Content-Type` being set with the [Media Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types) of `image/png`.

> `cross_origin` - `<string>` - Optional - The [CORS](https://developer.mozilla.org/en-US/docs/Glossary/CORS) setting to use when requesting the image. See  [HTMLImageElement.crossOrigin](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/crossOrigin) to see what values are allowed. Default is `"anonymous"`

) -> returns an `object` matching the message specification

Each call to the `fetch` method will send a new network request to `path`; it will not cache the results internally. If the correct HTTP header's in response the browser might cache the response to `path`; if this happens protopng will still reprocess the results as normal.

##### Nesting Messages
You can [nest](https://protobuf.dev/programming-guides/proto3/#nested) messages within each other. Here is a very simple example
```
const MessageA= protopng.message([
	protopng.string_field("exampleStringType" , 1),
]);
const MessageB= protopng.message([
	protopng.message("nestedA" , 1 , MessageB),
	protopng.messages("nestedARepeated" , 2 , MessageB),
]);
```

### Enumerations (Enums)
A basic Enum is following the same pattern as within [protobuf](https://protobuf.dev/programming-guides/proto3/#enum); this is that you have values (a string) and constants (a number). This method can be used in two ways, once to define an enum (we will cover that in this section) and secondly as a field in a message [(see fields)](#user-content-complex-fields). 

##### Defining an Enum
An Enum is defined as a a list of values and constants

`protopng.enum_field`(

> `values` - `<object>` or `<array>` - The list of values and constants within this Enum

) -> returns `protopng.enum_field` object

Array as an input expects:
`[ [ value <string> , constant <number> ] , ....]`
Object as an input expects:
`{ value <string> : constant <number> , ....}`

##### Examples
Defining an Enum using an `object` as input:
```
const Example= protopng.enum_field({
	"EXAMPLE_UNSPECIFIED":0,
	"EXAMPLE_A":1
});
```

Defining an Enum using an `array of arrays` as input
```
const Example= protopng.enum_field([
	["EXAMPLE_UNSPECIFIED" , 0],
	["EXAMPLE_A" , 1]
]);
```

### Fields
Protopng allows you to define the fields within messages to match any type that [protobuf has](https://protobuf.dev/programming-guides/proto3/#specifying-types). There is no way to define fields as optional since we treat all fields as optional. You can, and should, define a field as repeated, for each type there exists a singleton method and repeated method.

#### Simple Fields
`protopng.<method>`(

> `field_name` - `string` - The name and key of this field

> `field_number` - `number` - The integer number of this field

)

| Protobuf Type | Single Method  |  Repeated Method  | Returned JS Type [1] |
----------------|----------------|-------------------|----------------------|
| double        | double_field   | double_repeated   | Number               |
| float         | float_field    | float_repeated    | Number               |
| int32         | int32_field    | int32_repeated    | Number               |
| int64         | int64_field    | int64_repeated    | BigInt               |
| uint32        | uint32_field   | uint32_repeated   | Number               |   
| uint64        | uint64_field   | uint64_repeated   | BigInt               |
| sint32        | sint32_field   | sint32_repeated   | Number               |
| sint64        | sint64_field   | sint64_repeated   | BigInt               |
| fixed32       | fixed32_field  | fixed32_repeated  | Number               |
| fixed64       | fixed64_field  | fixed64_repeated  | BigInt               |
| sfixed32      | sfixed32_field | sfixed32_repeated | Number               |
| sfixed64      | sfixed64_field | sfixed64_repeated | BigInt               |
| bool          | bool_field     | bool_repeated     | Boolean              |
| string        | string_field   | string_repeated   | String               |
| bytes         | bytes_field    | bytes_repeated    | ArrayBuffer          |

- [1] A repeated field returns an Array of this type

##### Simple Fields Example
```
const MessageWithSimpleFields= protopng.message([
	protopng.string_field("exampleString" , 1),
	protopng.float_field("exampleFloat" , 2),
	protopng.bool_repeated("repeatedBooleans" , 3),
])
```

#### Complex Fields
These field types require a third parameter as part of it's definition
`protopng.<method>`(

> `field_name` - `string` - The name and key of this field

> `field_number` - `number` - The integer number of this field

> `additional_parameter` - `mixed` - Additional information needed to define this field

)
| Protobuf Type | Single Method  |  Repeated Method  | Returned JS Type [1] | Additional Parameter |
----------------|----------------|-------------------|----------------------|----------------------|
| map           | map_field      | N/A [2]           | Object               | Array [`key type` , `value type`] [3] |
| message       | message        | messages          | Object               | Defined `message` object or an `array of fields` [4] |
| enum          | enum_field     | enum_repeated     | String [5]           | Defined `enum_field` object, `value/constant object` [6] or an `array of values/constants` [7]

- [1] A repeated field returns an Array of this type
- [2] Map's can not be repeated in protobuf
- [3] Key type is one of `string_field`, `int32_field`, `int64_field`, `uint32_field`, `uint64_field`, `sint32_field`, `sint64_field`, `fixed32_field`, `sfixed32_field`, `fixed64_field`, `sfixed32_field` or `bool_field` . Value type can be any non-repeated type (excluding `map_field`).
- [4] See [defining a message](#defining-a-message) above for how to structure this array
- [5] The enum string value is returned. Unknown enum constants received will be cast to a string and also returned; this is following the [open enum](https://protobuf.dev/programming-guides/enum/) process
- [6] See [defining an enum](#defining-an-enum) above for how to structure this object
- [7] See [defining an enum](#defining-an-enum) above for how to structure this array

##### Map Field Example
You need to define the key type and value type of the items within the map. Protobuf does not allow multiple types as a value but does allow the value to be a message (where optional fields can be used).
```
const ExampleMessageWithMap= protopng.message([
	protopng.map_field("mapWithSimpleType" , 1 , [ protopng.string_field , protopng.uint32_field ] ),
	protopng.map_field("mapWithMessage" , 2 , [ protopng.string_field , AnotherDefinedMessage ] ),
])
```

## Handling of Unknown Fields
Any field encounted that is not in the definition defined above fails safe and is silently ignored. This can be used to your advantage to reduce the processing on the client if you are only interested in part of a message; however note the full protobuf payload is still downloaded to the client just not processed.
