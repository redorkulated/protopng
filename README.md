# Protopng
Providing a simple method to read protobuf data in the browser using PNGs as a transport method.

## Why?
PNG's are highly supported by every modern browser and come with many benefits such as caching. They also just so happen to be the perfect vessel to store random binary data; like protobuf data.

One of the objectives of this project was to make a lightweight way to encode and decode the data with no need for external packages.

## What?
Very simple example (taken from the [javascript](./packages/javascript/README.md) read me) :
```
import * as protopng from "./protopng/protopng.js"
const ExampleMessage= protopng.message([
	protopng.string_field("exampleStringType" , 1),
]);
ExampleTest.fetch("./example.png")
  .then((fetched_data)=>{ console.log(fetched_data); }
  .catch((process_error)=>console.error(process_error); }
```

## How?
With some simple wrapping of the protobuf payload and a simple client side library we are able to take our protobuf data, store it in an image and read it back:

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
- [python](./packages/python/README.md) 

## Specification
You can find the information on the latest protopng protocol V1 [here](./protocol/protocol-v1.md).

## Bug fixes, feature requests
Please do reach out if you spot any issues. Please however make sure you have read the read me files first to gain a basic understanding of this process.
