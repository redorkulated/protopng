export const proto= {
	"_varint32":(buffer,offset)=>{
		// Return a variable integer from the current buffer and return the new position in the buffer
		// Read byte by byte adding to the total
		// Using this large-code method (instead of a loop) to help heavily optimise this function
		// We take the lower 7 bits from each byte, shift it into the correct place, then add it to our result
		// Each row here is including one more byte of data
		if(!(buffer[0+offset] & 0x80)) return [offset+0+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))];
		if(!(buffer[1+offset] & 0x80)) return [offset+1+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))];
		if(!(buffer[2+offset] & 0x80)) return [offset+2+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))];
		if(!(buffer[3+offset] & 0x80)) return [offset+3+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))+((buffer[3+offset] & 0x7F) << ((8 * 3)-3))];
		if(!(buffer[4+offset] & 0x80)) return [offset+4+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))+((buffer[3+offset] & 0x7F) << ((8 * 3)-3))+((buffer[4+offset] & 0x7F) << ((8 * 4)-4))];
		if(!(buffer[5+offset] & 0x80)) return [offset+5+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))+((buffer[3+offset] & 0x7F) << ((8 * 3)-3))+((buffer[4+offset] & 0x7F) << ((8 * 4)-4))+((buffer[5+offset] & 0x7F) << ((8 * 5)-5))]
		if(!(buffer[6+offset] & 0x80)) return [offset+6+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))+((buffer[3+offset] & 0x7F) << ((8 * 3)-3))+((buffer[4+offset] & 0x7F) << ((8 * 4)-4))+((buffer[5+offset] & 0x7F) << ((8 * 5)-5))+((buffer[6+offset] & 0x7F) << ((8 * 6)-6))];
		if(!(buffer[7+offset] & 0x80)) return [offset+7+1,((buffer[0+offset] & 0x7F) << ((8 * 0)-0))+((buffer[1+offset] & 0x7F) << ((8 * 1)-1))+((buffer[2+offset] & 0x7F) << ((8 * 2)-2))+((buffer[3+offset] & 0x7F) << ((8 * 3)-3))+((buffer[4+offset] & 0x7F) << ((8 * 4)-4))+((buffer[5+offset] & 0x7F) << ((8 * 5)-5))+((buffer[6+offset] & 0x7F) << ((8 * 6)-6))+((buffer[7+offset] & 0x7F) << ((8 * 7)-7))];

		// Varint larger than 8 bytes, fall back to the slow and steady method
		for(let return_integer=0,byte_offset=0;;byte_offset++){
			// Read the lower 7 bits of our byte and shift them into position
			return_integer+= ((buffer[offset + byte_offset] & 0x7F) << ((8 * byte_offset) - byte_offset));

			// If the high bit is set then this was our last byte
			if(!(buffer[offset + byte_offset] & 0x80)) return [offset + byte_offset + 1,return_integer];
		}
	},
	"_varint64":(buffer,offset)=>{
		// Return a variable 64-bit integer from the current buffer and return the new position in the buffer
		// Read byte by byte adding to the total
		// Using this large-code method (instead of a loop) to help heavily optimise this function
		// We take the lower 7 bits from each byte, shift it into the correct place, then add it to our result
		// Each row here is including one more byte of data
		if(!(buffer[0+offset] & 0x80)) return [offset+0+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))];
		if(!(buffer[1+offset] & 0x80)) return [offset+1+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))];
		if(!(buffer[2+offset] & 0x80)) return [offset+2+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))];
		if(!(buffer[3+offset] & 0x80)) return [offset+3+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))+(BigInt(buffer[3+offset] & 0x7F) << ((8n * 3n)-3n))];
		if(!(buffer[4+offset] & 0x80)) return [offset+4+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))+(BigInt(buffer[3+offset] & 0x7F) << ((8n * 3n)-3n))+(BigInt(buffer[4+offset] & 0x7F) << ((8n * 4n)-4n))];
		if(!(buffer[5+offset] & 0x80)) return [offset+5+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))+(BigInt(buffer[3+offset] & 0x7F) << ((8n * 3n)-3n))+(BigInt(buffer[4+offset] & 0x7F) << ((8n * 4n)-4n))+(BigInt(buffer[5+offset] & 0x7F) << ((8n * 5n)-5n))]
		if(!(buffer[6+offset] & 0x80)) return [offset+6+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))+(BigInt(buffer[3+offset] & 0x7F) << ((8n * 3n)-3n))+(BigInt(buffer[4+offset] & 0x7F) << ((8n * 4n)-4n))+(BigInt(buffer[5+offset] & 0x7F) << ((8n * 5n)-5n))+(BigInt(buffer[6+offset] & 0x7F) << ((8n * 6n)-6n))];
		if(!(buffer[7+offset] & 0x80)) return [offset+7+1,(BigInt(buffer[0+offset] & 0x7F) << ((8n * 0n)-0n))+(BigInt(buffer[1+offset] & 0x7F) << ((8n * 1n)-1n))+(BigInt(buffer[2+offset] & 0x7F) << ((8n * 2n)-2n))+(BigInt(buffer[3+offset] & 0x7F) << ((8n * 3n)-3n))+(BigInt(buffer[4+offset] & 0x7F) << ((8n * 4n)-4n))+(BigInt(buffer[5+offset] & 0x7F) << ((8n * 5n)-5n))+(BigInt(buffer[6+offset] & 0x7F) << ((8n * 6n)-6n))+(BigInt(buffer[7+offset] & 0x7F) << ((8n * 7n)-7n))];

		// Varint larger than 8 bytes, fall back to the slow and steady method
		for(let return_integer=0n,byte_offset=0;;byte_offset++){
			// Read the lower 7 bits of our byte and shift them into position
			return_integer+= (BigInt(buffer[offset + byte_offset] & 0x7F) << BigInt((8 * byte_offset) - byte_offset));

			// If the high bit is set then this was our last byte
			if(!(buffer[offset + byte_offset] & 0x80)) return [offset + byte_offset + 1,return_integer];
		}
	},
	"WIRETYPE_VARINT":0,
	"WIRETYPE_I64":1,
	"WIRETYPE_LEN":2,
	"WIRETYPE_I32":5,
	"root":(buffer,offset,length,fields)=>{
		return proto.message(buffer,offset,length,fields,proto.WIRETYPE_LEN)[1]
	},
	"message":(buffer,offset,length,fields,wiretype)=>{
		let msg= {};
		let offset_end= offset + length;
		let cur_offset= offset_end;
		while(offset < offset_end){
			if(offset === cur_offset || offset < 0){
				throw `Malformed payload received; can not process`
			}
			cur_offset= offset;

			// Read the field header details
			let field_header= 0;
			[offset,field_header]= proto._varint32(buffer,offset);
			let field_wiretype= field_header & 0x07;
			let field_no= (field_header >> 3);
			let details= fields[field_no];

			// Unknown field, allow us to parse but ignore
			if(details === undefined){
				fields[field_no]= {
					"type":"unknown",
					"handler":proto.placeholder,
					"field_number":field_no,
				};
				details= fields[field_no];
			}

			// Ensure output is an object
			if(
				details.field_name !== undefined
				&& msg[details.field_name] === undefined
				&& details.type === "map"
				&& details.repeated
			){
				msg[details.field_name]= {};
			}

			// Ensure output is an array
			else if(
				details.field_name !== undefined
				&& msg[details.field_name] === undefined
				&& details.repeated
			){
				msg[details.field_name]= [];
			}

			// Var Type : Get data length
			let field_length= 0;
			if(field_wiretype === proto.WIRETYPE_LEN){
				[offset,field_length]= proto._varint32(buffer,offset);
				if(field_length === undefined) return [offset,msg];
			}

			let processed_value= undefined;
			if(details.handler === undefined) return [offset,msg];
			[offset,processed_value]= details.handler(buffer,offset,field_length,details.fields,field_wiretype);

			// Field is unknown, discard this value
			if(details.field_name === undefined){ /* Do nothing */ }

			// Value returned is within a map, add to object
			else if(details.repeated && processed_value !== undefined && details.type === "map") msg[details.field_name][processed_value.k]= processed_value.v

			// Value returned is an array, concat it to our existing array
			else if(details.repeated && processed_value !== undefined && Array.isArray(processed_value)) msg[details.field_name]= msg[details.field_name].concat(processed_value)

			// Value returned is single but belongs in an array, push it into our existing array
			else if(details.repeated && processed_value !== undefined) msg[details.field_name].push(processed_value)

			// Field is single, set our value, this will overwrite a already received value if sent twice (Which should not happen)
			else if(processed_value !== undefined) msg[details.field_name]= processed_value
		}

		return [offset,msg]
	},
	"enum":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint32(buffer,offset);
				ra.push(fields[rv] === undefined ? rv.toString() : fields[rv])
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint32(buffer,offset);
		return [offset,fields[rv] === undefined ? rv.toString() : fields[rv]];
	},
	"uint32":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint32(buffer,offset);
				ra.push(rv)
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint32(buffer,offset);
		return [offset,rv];
	},
	"int32":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint32(buffer,offset);
				// Un-twos-compliment the number back to the original number
				rv= rv & 0x80000000 ? (((rv & 0xffffffff) ^ 0x80000000) - 0x80000000) : rv;
				ra.push(rv);
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint32(buffer,offset);
		// Un-twos-compliment the number back to the original number
		rv= rv & 0x80000000 ? (((rv & 0xffffffff) ^ 0x80000000) - 0x80000000) : rv;
		return [offset,rv];
	},
	"sint32":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint32(buffer,offset);
				// Un-zig-zag the number back to the original number
				rv= ((rv >> 1) ^ -(rv & 1));
				ra.push(rv);
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint32(buffer,offset);
		// Un-zig-zag the number back to the original number
		rv= ((rv >> 1) ^ -(rv & 1));
		return [offset,rv];
	},
	"uint64":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint64(buffer,offset);
				ra.push(rv)
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint64(buffer,offset);
		return [offset,rv];
	},
	"int64":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint64(buffer,offset);
				// Un-twos-compliment the number back to the original number
				rv= rv & 0x8000000000000000n ? (((rv & 0xffffffffffffffffn) ^ 0x8000000000000000n) - 0x8000000000000000n) : rv;
				ra.push(rv);
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint64(buffer,offset);
		// Un-twos-compliment the number back to the original number
		rv= rv & 0x8000000000000000n ? (((rv & 0xffffffffffffffffn) ^ 0x8000000000000000n) - 0x8000000000000000n) : rv;
		return [offset,rv];
	},
	"sint64":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint64(buffer,offset);
				// Un-zig-zag the number back to the original number
				rv= ((rv >> 1n) ^ -(rv & 1n));
				ra.push(rv);
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint64(buffer,offset);
		// Un-zig-zag the number back to the original number
		rv= ((rv >> 1n) ^ -(rv & 1n));
		return [offset,rv];
	},
	"string":(buffer,offset,length,fields,wiretype)=>{
		return [offset + length,(new TextDecoder()).decode(buffer.slice(offset,length+offset))];
	},
	"bytes":(buffer,offset,length,fields,wiretype)=>{
		return [offset + length,buffer.slice(offset,length+offset).buffer];
	},
	"bool":(buffer,offset,length,fields,wiretype)=>{
		let rv= undefined;
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				[offset,rv]= proto._varint32(buffer,offset);
				rv= rv?true:false
				ra.push(rv)
			}
			return [offset,ra];
		}
		[offset,rv]= proto._varint32(buffer,offset);
		rv= rv?true:false
		return [offset,rv];
	},
	"_buffer":(buffer,offset,length,fields,wiretype,get_type,get_width)=>{
		let rv= undefined;
		let bufferview= new DataView(buffer.buffer)
		if(wiretype === proto.WIRETYPE_LEN){
			let offset_end= offset + length;
			let ra= [];
			while(offset < offset_end){
				// Read our encoded type as little-endian
				ra.push(bufferview[get_type](offset,true))
				offset+= get_width
			}
			return [offset,ra];
		}

		return [
			offset + get_width,
			bufferview[get_type](offset,true)
		];
	},
	"fixed32":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getUint32",4),
	"fixed64":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getBigUint64",8),
	"sfixed32":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getInt32",4),
	"sfixed64":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getBigInt64",8),
	"float":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getFloat32",4),
	"double":(buffer,offset,length,fields,wiretype)=>proto._buffer(buffer,offset,length,fields,wiretype,"getFloat64",8),
	"placeholder":(buffer,offset,length,fields,wiretype)=>{
		// This Placeholder hander is used when we read a field we do not know what it is
		// We use the wiretype to skip past it
		if(wiretype === proto.WIRETYPE_LEN) return [offset + length,undefined];
		if(wiretype === proto.WIRETYPE_I32) return [offset + 4,undefined];
		if(wiretype === proto.WIRETYPE_I64) return [offset + 8,undefined];
		if(wiretype === proto.WIRETYPE_VARINT){
			// Varint
			let _= undefined;
			[offset,_]= proto._varint32(buffer,offset);
			return [offset,undefined];
		}
		throw `Can not decode protobuf payload; unknown wiretype ${wiretype} encounted`;
	},
};
