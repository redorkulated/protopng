import * as protopng from "./protopng/protopng.js"

const Letters= protopng.enum_field({
	"LETTER_UNSPECIFIED":0,
	"LETTER_A":1,
	"LETTER_B":2,
	"LETTER_C":3,
	"LETTER_D":4
});

const ExampleNested= protopng.message([
	protopng.string_field("exampleStringType",1),
	protopng.bytes_field("exampleBytesType",2),
	protopng.int32_field("exampleInt32Type",3),
	protopng.uint32_field("exampleUInt32Type",4),
	protopng.sint32_field("exampleSInt32Type",5),
	protopng.int64_field("exampleInt64Type",6),
	protopng.uint64_field("exampleUInt64Type",7),
	protopng.sint64_field("exampleSInt64Type",8),
	protopng.bool_field("exampleBoolType",9),
	protopng.fixed32_field("exampleFixed32Type",10),
	protopng.fixed64_field("exampleFixed64Type",11),
	protopng.sfixed32_field("exampleSFixed32Type",12),
	protopng.sfixed64_field("exampleSFixed64Type",13),
	protopng.float_field("exampleFloatType",14),
	protopng.double_field("exampleDoubleType",15),
	protopng.enum_field("exampleEnumType",17,{"LETTER_UNSPECIFIED":0,"LETTER_A":1,"LETTER_B":2,"LETTER_C":3,"LETTER_D":4}),

	protopng.string_repeated("exampleRepeatedStringType",21),
	protopng.bytes_repeated("exampleRepeatedBytesType",22),
	protopng.int32_repeated("exampleRepeatedInt32Type",23),
	protopng.uint32_repeated("exampleRepeatedUInt32Type",24),
	protopng.sint32_repeated("exampleRepeatedSInt32Type",25),
	protopng.int64_repeated("exampleRepeatedInt64Type",26),
	protopng.uint64_repeated("exampleRepeatedUInt64Type",27),
	protopng.sint64_repeated("exampleRepeatedSInt64Type",28),
	protopng.bool_repeated("exampleRepeatedBoolType",29),
	protopng.fixed32_repeated("exampleRepeatedFixed32Type",30),
	protopng.fixed64_repeated("exampleRepeatedFixed64Type",31),
	protopng.sfixed32_repeated("exampleRepeatedSFixed32Type",32),
	protopng.sfixed64_repeated("exampleRepeatedSFixed64Type",33),
	protopng.float_repeated("exampleRepeatedFloatType",34),
	protopng.double_repeated("exampleRepeatedDoubleType",35),
	protopng.enum_repeated("exampleRepeatedEnumType",37,Letters),

	protopng.string_field("exampleBigFieldID",1337),
]);

const ExampleTest= protopng.message([
	protopng.string_field("exampleTestString",1),
	protopng.messages("exampleRepeatedMessage",4,[
		protopng.string_field("exampleStringType",1),
		protopng.bytes_field("exampleBytesType",2),
		protopng.int32_field("exampleInt32Type",3),
		protopng.uint32_field("exampleUInt32Type",4),
		protopng.sint32_field("exampleSInt32Type",5),
		protopng.int64_field("exampleInt64Type",6),
		protopng.uint64_field("exampleUInt64Type",7),
		protopng.sint64_field("exampleSInt64Type",8),
		protopng.bool_field("exampleBoolType",9),
		protopng.fixed32_field("exampleFixed32Type",10),
		protopng.fixed64_field("exampleFixed64Type",11),
		protopng.sfixed32_field("exampleSFixed32Type",12),
		protopng.sfixed64_field("exampleSFixed64Type",13),
		protopng.float_field("exampleFloatType",14),
		protopng.double_field("exampleDoubleType",15),
		protopng.map_field("exampleMapType",16,[protopng.string_field,ExampleNested]),
		protopng.enum_field("exampleEnumType",17,Letters),

		protopng.string_repeated("exampleRepeatedStringType",21),
		protopng.bytes_repeated("exampleRepeatedBytesType",22),
		protopng.int32_repeated("exampleRepeatedInt32Type",23),
		protopng.uint32_repeated("exampleRepeatedUInt32Type",24),
		protopng.sint32_repeated("exampleRepeatedSInt32Type",25),
		protopng.int64_repeated("exampleRepeatedInt64Type",26),
		protopng.uint64_repeated("exampleRepeatedUInt64Type",27),
		protopng.sint64_repeated("exampleRepeatedSInt64Type",28),
		protopng.bool_repeated("exampleRepeatedBoolType",29),
		protopng.fixed32_repeated("exampleRepeatedFixed32Type",30),
		protopng.fixed64_repeated("exampleRepeatedFixed64Type",31),
		protopng.sfixed32_repeated("exampleRepeatedSFixed32Type",32),
		protopng.sfixed64_repeated("exampleRepeatedSFixed64Type",33),
		protopng.float_repeated("exampleRepeatedFloatType",34),
		protopng.double_repeated("exampleRepeatedDoubleType",35),
		protopng.enum_repeated("exampleRepeatedEnumType",37,Letters),

		protopng.message("exampleNestedMessage",42,ExampleNested),

		protopng.string_field("exampleBigFieldID",300),
	])
]);

window.addEventListener("load",()=>{
	// Where do we need to read the data from?
	const test_file="./01-ExampleNested.png";

	// Actually fetch the data using our protobuf message specification "ExampleTest"
	ExampleTest.fetch(test_file)
	.then((fetched_data)=>{
		//
		// Here you would use the fetched_data within your normal application flow
		//

		// As a test demonstration we will output the fetched_data to the browser for inspection
		document.body.innerHTML=`<h1>Data successfully read from '${test_file}'</h1>`;
		let s= document.createElement('style');
		s.appendChild(document.createTextNode(`
			body{ font-family:monospace;overflow-wrap:break-word; }
			div{ display:grid;grid-template-columns:10rem 1fr;grid-auto-flow:row dense;grid-gap:0.5rem; }
			div,span{ padding:2px;border:1px solid #333; }
			div:nth-child(2n+1),span:nth-child(2n+1){ font-weight:bold; }
			div:nth-child(2n+2),span:nth-child(2n+2){ font-weight:normal !important; }
		`));
		document.head.append(s);
		const debug= (parent,title,data)=>{
			let fragment= document.createDocumentFragment();
			let title_element= document.createElement(title === undefined ? "hr" : "span");
			parent= title === undefined ? "" : parent +"."+ title +" ("+ data.constructor.name +")";
			title_element.innerText= title === undefined ? "" : title; title_element.title= title === undefined ? "" : parent;
			let container= document.createElement(["string","number","bigint","boolean"].indexOf(typeof data) !== -1 || data.constructor.name === "ArrayBuffer" ? "span" : "div");
			if(data.constructor.name === "ArrayBuffer") container.innerText= Array.from(new Uint8Array(data)).map((q)=>q.toString(16).padStart(2,"0")).join(" ").toLowerCase();
			else if(typeof data == "string" || typeof data == "number" || typeof data === "bigint" || typeof data === "boolean") container.innerText= data;
			else if(Array.isArray(data) && data.length) container.append(...(data.map((q,i)=>debug(parent,`[${i}]`,q))));
			else if(typeof data === "object" && Object.keys(data).length) container.append(...(Object.keys(data).map((q)=>debug(parent,q,data[q]))));
			else if(Array.isArray(data) || typeof data === "object") container.innerHTML="<i>Empty</i>";
			else container.innerText="UNKNOWN";
			fragment.append(title_element,container);
			return fragment;
		};
		document.body.append(debug(undefined,undefined,fetched_data));
	})
	.catch((process_error)=>document.body.innerText=`Error while reading ExampleTest from '${test_file}' : '${process_error}'`);
});
