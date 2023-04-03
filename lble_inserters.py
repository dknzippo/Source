def Int8ToUint8(v):
	if v < 0:
		v = (256 + v) % 256
	return v
	   
def Int16ToUint16(v):
	if v < 0:
		v = (65536 + v) % 65536
	return v

def Int32ToUint32(v):
	if v < 0:
		v = (4294967296 + v) % 4294967296
	return v
	
def InsertString(b,o,s):
	ExtendBuffer(b,o,len(s))
	for i in range(len(s)):
		b[o + i] = ord(s[i])
	
def InsertStringWithChecksum(b,o,s):
	ExtendBuffer(b,o,len(s) + 1)
	chksum = 0
	for i in range(len(s)):
		chksum ^= ord(s[i])
	for i in range(len(s)):
		b[o + i] = ord(s[i])
	b[o + len(s)] = chksum ^ 0xFF
	
def InsertUint8(b,o,v):
	ExtendBuffer(b,o,1)
	v = v % 256
	b[o] = v

def InsertInt8(b,o,v):
	ExtendBuffer(b,o,1)
	b[o] = Int8ToUint8(v)

def InsertInt8Array(b,o,a):
	ExtendBuffer(b,o,len(a))
	for i in range(len(a)):
		b[o + i] = Int8ToUint8(a[i])
	
def InsertInt16(b,o,v):
	ExtendBuffer(b,o,2)
	cv = Int16ToUint16(v)
	b[o] = (cv & 0xFF)
	b[o + 1] = ((cv>>8) & 0xFF)
	
def InsertInt32(b,o,v):
	ExtendBuffer(b,o,4)
	cv = Int32ToUint32(v)
	b[o] = (cv & 0xFF)
	b[o + 1] = ((cv>>8) & 0xFF)
	b[o + 2] = ((cv>>16) & 0xFF)	
	b[o + 3] = ((cv>>24) & 0xFF)
	
def InsertUint32(b,o,v):
	ExtendBuffer(b,o,4)
	b[o] = (v & 0xFF)
	b[o + 1] = ((v>>8) & 0xFF)
	b[o + 2] = ((v>>16) & 0xFF)	
	b[o + 3] = ((v>>24) & 0xFF)

def ExtendBuffer(b,o,s):
	if len(b) <= o + s:
		b.extend([0 for i in range(o - len(b) + s)])	

inserter =  { 'string':			 	InsertString
			, 'string_cs':		  	InsertStringWithChecksum
			, 'uint8':			  	InsertUint8
			, 'int8':			   	InsertInt8
			, 'int8[]':			 	InsertInt8Array
#			, 'LEGOversion':		InsertLEGOVersion
#			, 'uint16':				InsertUint16
			, 'int16':				InsertInt16
			, 'uint32':				InsertUint32
			, 'int32':				InsertInt32
#			, 'float32':			InsertFloat32
#			, 'BluetoothMAC':		InsertBluetoothMAC
#			, 'IOTypeID':			InsertIOTypeID
#			, 'ModeCombinations':	InsertModeCombinations
			}