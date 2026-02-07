# Protopng
Providing a simple method to read [protobuf](https://protobuf.dev/) data in the browser using [PNGs](https://www.w3.org/TR/2003/REC-PNG-20031110/) as a transport method.

## Why?
PNG's are highly supported by every modern browser and come with many benefits such as caching. They also just so happen to be the perfect vessel to store random binary data; like protobuf data.

One of the objectives of this project was to make a lightweight way to encode and decode the data with no need for external packages.

Using protobuf over pure JSON allows for the same data to be transmitted with much less overhead over the network. Based on the [example test](./tests/python3/01-ExampleNested.py) image below we are able to transmit a 13kb PNG payload instead of a 95kb JSON payload:
```
JSON byte length : 97603 bytes (95.32 kb, 0.09 mb)
Protobuf byte length : 14161 bytes (13.83 kb, 0.01 mb)
 ... -85.49%% compared to the JSON byte length
Protopng byte length : 13519 bytes (13.2 kb, 0.01 mb)
 ... -86.15%% compared to the JSON byte length
 ... -4.53%% compared to the protobuf byte length
```

## What?
A very simple example (taken from the [javascript](./packages/javascript/README.md) read me) :
```
import * as protopng from "./protopng/protopng.js"
const ExampleMessage= protopng.message([
	protopng.string_field("exampleStringType" , 1),
]);
ExampleTest.fetch("./example.png")
  .then((fetched_data)=>{ console.log(fetched_data); })
  .catch((process_error)=>{ console.error(process_error); })
```

## How?
With some lightweight wrapping of the protobuf payload, for example via the [python library](./packages/python3), we are able to store it in a PNG image and decompile it back within the browser:

Our image :

![example protopng](./tests/javascript/01-ExampleNested.png)

... becomes ...
```
{
  "exampleRepeatedMessage": [
    {
      "exampleInt32Type": -20822023,
      "exampleUInt32Type": 25457276,
      "exampleSInt32Type": -55682617,
      "exampleSInt64Type": 4082124483394558882,
      "exampleFixed32Type": 2481122489,
      ....
    }
  ]
}
```

## Packaged Libraries
You can find all the details on how to use protopng within the specific language's read me
- [javascript](./packages/javascript/README.md) 
- [python3](./packages/python3/README.md)

## Specification
You can find the information on the latest protopng protocol V1 [here](./protocol/protocol-v1.md).

## Bug fixes, feature requests
Please do reach out if you spot any issues. Please however make sure you have read the read me files first to gain a basic understanding of this process.
