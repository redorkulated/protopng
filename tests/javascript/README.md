# Javscript Tests

## 01-ExampleNested
Simple test to read the output protopng created by the [python3 tests](../python3/). This test is based on the protobuf specification file [01-ExampleNested.proto](../protobuf/01-ExampleNested.proto).

It is designed to cover all the [field types](https://protobuf.dev/programming-guides/proto3/#specifying-types) available within protobuf and complex operations such as repeated fields and nesting of messages.

#### How to Run
###### Setup the file structure like this within a directory on a webserver
 - [./01-ExampleNested.html](./01-ExampleNested.html)
 - [./01-ExampleNested.js](./01-ExampleNested.js)
 - [./01-ExampleNested.png](../python3/output/01-ExampleNested.png)
 - [./protopng](../../packages/javascript/protopng)

###### Open `https://<path/to/your>/01-ExampleNested.html`
The `01-ExampleNested.html` file must be opened via localhost or a HTTPS context to overcome modern security checks in browsers (For example [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)).

#### Expected Output
You should now see the output of the protopng file displayed; comparisons can now be made to the source data.
