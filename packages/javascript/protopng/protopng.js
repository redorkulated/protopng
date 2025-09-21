import {proto} from "./proto.js"
const _message_fetch= async function(path,cross_origin){
	return new Promise((resolve_callback,reject_callback)=>{
		let base_image= new Image();
		base_image.crossOrigin= cross_origin === undefined ? "anonymous" : cross_origin;
		base_image.addEventListener("error",()=>{
			reject_callback("Network error");
		});
		base_image.addEventListener("load",()=>{
			// Setup our canvas and put our "image" onto it
			let canvas_element= document.createElement("canvas");
			let canvas_context= canvas_element.getContext("2d",{"willReadFrequently":true});
			canvas_element.width= base_image.width;
			canvas_element.height= base_image.height;
			canvas_context.drawImage(base_image,0,0);

			// Read the pixels as bytes, skipping every 4th byte (the alpha-channel byte) as these are undefined bytes
			let raw_data= canvas_context.getImageData(0,0,base_image.width,base_image.height).data.filter((v,i)=>(i+1) % 4);

			// Read our Version integer
			let data_read_offset= 0;
			let protocol_version= 0;
			let payload_length= 0;
			[data_read_offset,protocol_version]= proto._varint32(raw_data,data_read_offset);

			// Protocol Version 1
			// Fields [Payload Length,Original Payload...]
			if(protocol_version === 1){
				// Read the payload length
				[data_read_offset,payload_length]= proto._varint32(raw_data,data_read_offset);
			}

			// Unknown version
			else{
				reject_callback(`Unknown protopng protocol version '${protocol_version}' in '${path}'`);
				return;
			}

			// Process the protobuf payload starting from the current payload-offset iwth the given payload-length
			let processed_data;
			try{
				processed_data= proto.root(raw_data,data_read_offset,payload_length,this.fields);
			}catch(e){
				reject_callback(e);
				return;
			}

			// Return our data
			resolve_callback(processed_data);
		});
		base_image.src= path;
	});
};

const _message= (field_name,field_number,fields,repeated)=>{
	// Just fields in an array
	// - (<Fields>)
	// This method is used when defining a Message without linking it to a field
	if(
		field_name !== undefined
		&& Array.isArray(field_name)
	){
		fields= field_name;
		field_name= undefined;
		field_number= undefined;
		repeated= false;
	}

	// We have an array of fields as the last parameter
	// - (<Field Name>, <Field Number>, <Fields>)
	else if(
		field_name !== undefined
		&& field_number !== undefined
		&& fields !== undefined
		&& Array.isArray(fields)
	){
		repeated= repeated === true;
	}

	// We have a message as the last parameter
	// - (<Field Name>, <Field Number>, <Message()>)
	else if(
		field_name !== undefined
		&& field_number !== undefined
		&& fields !== undefined
		&& fields.fields !== undefined
		&& Array.isArray(fields.fields)
	){
		repeated= repeated === true;
		fields= fields.fields;
	}

	// Unknown usage
	else{
		throw "protopng.message provided incorrect parameters";
		return;
	}

	// Convert the array of fields provided to be a sparse array with field numbers as indexes
	let return_fields= [];
	fields.forEach((f)=>{
		if(f === undefined || f.field_number === undefined) return;
		if(return_fields[f.field_number] !== undefined) throw `field number ${f.field_number} defined twice : "${return_fields[f.field_number].field_name}" and "${f.field_name}"`;
		return_fields[f.field_number]= f;
	});

	return {
		"type":"message",
		"handler":proto.message,
		"fields":return_fields,
		"field_name":field_name,
		"field_number":field_number,
		"repeated":repeated,
		"fetch":repeated ? undefined : _message_fetch
	};
};
export const message= (field_name,field_number,fields)=>_message(field_name,field_number,fields,false);
export const messages= (field_name,field_number,fields)=>_message(field_name,field_number,fields,true);
export const message_field= message;
export const message_repeated= messages;

const _enum= (field_name,field_number,fields,repeated)=>{
	// Just fields in an array or an object
	// - (<fields>)
	// This method is used when defining an Enum without linking it to a field
	if(
		field_name !== undefined
		&& field_number === undefined
		&& (
			// Normal array
			Array.isArray(field_name)

			// Dict key->value
			|| (
				typeof field_name === "object"
				&& Object.keys(field_name).length > 0
				&& Object.keys(field_name).map((x)=>typeof field_name[x]).reduce((e,n) =>e && n, true)
			)
		)
	){
		fields= field_name;
		field_name= undefined;
		field_number= undefined;
		repeated= false;
	}

	// We have an array of fields, a dict of fields or an existing enum as the last parameter
	// - (<Field Name>, <Field Number>, <Fields>)
	else if(
		field_name !== undefined
		&& field_number !== undefined
		&& fields !== undefined
		&& (
			// Normal array [[k,v],....]
			(
				Array.isArray(fields)
				&& fields.length > 0
				&& fields.map((x)=>x.length === 2 && typeof x[0] === "string" && typeof x[1] === "number").reduce((e,n) =>e && n, true)
			)

			// Dict key->value
			|| (
				typeof fields === "object"
				&& Object.keys(fields).length > 0
				&& Object.keys(fields).map((x)=>typeof x === "string" && typeof fields[x] === "number").reduce((e,n) =>e && n, true)
			)

			// Existing enum_field
			|| (
				typeof fields === "object"
				&& fields.type === "enum"
				&& fields.fields !== undefined
			)
		)
	){
		repeated= repeated === true;
	}

	// Unknown usage
	else{
		throw "protopng.enum_field provided incorrect parameters";
		return;
	}

	// Convert the array or dict of fields provided to be a sparse array with field numbers as indexes
	let return_fields= [];
	if(typeof fields === "object" && fields.type === "enum" && fields.fields !== undefined){
		// Get the existing fields from our exiting enum
		 return_fields= fields.fields;
	}else if(Array.isArray(fields)){
		// Convert from k,v structure
		fields.forEach((f)=>{
			if(f === undefined || f[0] === undefined || f[1] === undefined) return;
			return_fields[f[1]]= f[0];
		});
	}else{
		// Convert from k=>v structure
		Object.keys(fields).forEach((x)=>{
			if(fields[x] === undefined) return;
			return_fields[fields[x]]= x;
		});
	}

	return {
		"type":"enum",
		"handler":proto.enum,
		"fields":return_fields,
		"field_name":field_name,
		"field_number":field_number,
		"repeated":repeated,
	};
};
export const enum_field= (field_name,field_number,fields)=>_enum(field_name,field_number,fields,false);
export const enum_repeated= (field_name,field_number,fields)=>_enum(field_name,field_number,fields,true);

export const map_field= (field_name,field_number,key_value_types)=>{
	if(key_value_types === undefined) throw `Key/Value types not provided`;
	// Key types can only be basic single scalar types
	if(!(
		key_value_types[0] === string_field || key_value_types[0] === bool_field
		|| key_value_types[0] === int32_field || key_value_types[0] === int64_field
		|| key_value_types[0] === uint32_field || key_value_types[0] === uint64_field
		|| key_value_types[0] === sint32_field || key_value_types[0] === sint64_field
		|| key_value_types[0] === fixed32_field || key_value_types[0] === sfixed32_field
		|| key_value_types[0] === fixed64_field || key_value_types[0] === sfixed64_field
	)){
		throw `Map key type can only be one of string_field, int32_field, int64_field, uint32_field, uint64_field, sint32_field, sint64_field, fixed32_field, sfixed32_field, fixed64_field, sfixed32_field or bool_field`;
	}

	// fields can be any single type but not a map
	if(!(
		key_value_types[1] === string_field || key_value_types[1] === bool_field || key_value_types[1] === bytes_field
		|| key_value_types[1] === int32_field || key_value_types[1] === int64_field
		|| key_value_types[1] === uint32_field || key_value_types[1] === uint64_field
		|| key_value_types[1] === sint32_field || key_value_types[1] === sint64_field
		|| key_value_types[1] === fixed32_field || key_value_types[1] === sfixed32_field
		|| key_value_types[1] === fixed64_field || key_value_types[1] === sfixed64_field
		|| key_value_types[1] === float_field || key_value_types[1] === double_field
		|| key_value_types[1] == enum_field
		|| (typeof key_value_types[1] === "object" && key_value_types[1].type === "message")
	)){
		throw `Map value type must be a non-repeated field, non-repeated message or non-repeated enum`;
	}

	return {
		"type":"map",
		"handler":proto.message,
		"fields":message(
			field_name,
			field_number,
			[
				key_value_types[0]("k",1),
				typeof key_value_types[1] === "object" && key_value_types[1].type === "message" ? message("v",2,key_value_types[1]) : key_value_types[1]("v",2)
			]
		).fields,
		"field_name":field_name,
		"field_number":field_number,
		"repeated":true,
	};
}

const _generic= (_type,field_name,field_number,repeated)=>(
	{
		"type":_type,
		"handler":proto[_type],
		"field_name":field_name,
		"field_number":field_number,
		"repeated":repeated === true
	}
);

export const string_field= (field_name,field_number)=>_generic("string",field_name,field_number);
export const string_repeated= (field_name,field_number)=>_generic("string",field_name,field_number,true);

export const bytes_field= (field_name,field_number)=>_generic("bytes",field_name,field_number);
export const bytes_repeated= (field_name,field_number)=>_generic("bytes",field_name,field_number,true);

export const int32_field= (field_name,field_number)=>_generic("int32",field_name,field_number);
export const int32_repeated= (field_name,field_number)=>_generic("int32",field_name,field_number,true);
export const int64_field= (field_name,field_number)=>_generic("int64",field_name,field_number);
export const int64_repeated= (field_name,field_number)=>_generic("int64",field_name,field_number,true);

export const uint32_field= (field_name,field_number)=>_generic("uint32",field_name,field_number);
export const uint32_repeated= (field_name,field_number)=>_generic("uint32",field_name,field_number,true);
export const uint64_field= (field_name,field_number)=>_generic("uint64",field_name,field_number);
export const uint64_repeated= (field_name,field_number)=>_generic("uint64",field_name,field_number,true);

export const sint32_field= (field_name,field_number)=>_generic("sint32",field_name,field_number);
export const sint32_repeated= (field_name,field_number)=>_generic("sint32",field_name,field_number,true);
export const sint64_field= (field_name,field_number)=>_generic("sint64",field_name,field_number);
export const sint64_repeated= (field_name,field_number)=>_generic("sint64",field_name,field_number,true);

export const bool_field= (field_name,field_number)=>_generic("bool",field_name,field_number);
export const bool_repeated= (field_name,field_number)=>_generic("bool",field_name,field_number,true);

export const fixed32_field= (field_name,field_number)=>_generic("fixed32",field_name,field_number);
export const fixed32_repeated= (field_name,field_number)=>_generic("fixed32",field_name,field_number,true);

export const fixed64_field= (field_name,field_number)=>_generic("fixed64",field_name,field_number);
export const fixed64_repeated= (field_name,field_number)=>_generic("fixed64",field_name,field_number,true);

export const sfixed32_field= (field_name,field_number)=>_generic("sfixed32",field_name,field_number);
export const sfixed32_repeated= (field_name,field_number)=>_generic("sfixed32",field_name,field_number,true);

export const sfixed64_field= (field_name,field_number)=>_generic("sfixed64",field_name,field_number);
export const sfixed64_repeated= (field_name,field_number)=>_generic("sfixed64",field_name,field_number,true);

export const float_field= (field_name,field_number)=>_generic("float",field_name,field_number);
export const float_repeated= (field_name,field_number)=>_generic("float",field_name,field_number,true);

export const double_field= (field_name,field_number)=>_generic("double",field_name,field_number);
export const double_repeated= (field_name,field_number)=>_generic("double",field_name,field_number,true);
