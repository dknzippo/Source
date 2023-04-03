import struct

_ioTypeID_lookup = {
	0x0001: 'Motor'
  , 0x0005: 'Button'
  , 0x0014: 'Voltage'
  , 0x0015: 'Current'
  , 0x0016: 'Piezo Tone (Sound)'
  , 0x0017: 'RGB Light'
  , 0x0022: 'External Tilt Sensor'
  , 0x0023: 'Motion Sensor'
  , 0x0025: 'Vision Sensor'
  , 0x0026: 'External Motor with Tacho'
  , 0x0027: 'Internal Motor with Tacho'
  , 0x0028: 'Internal Tilt'
	}

def ExtractString(b,d):
	value = ''.join(map(chr, b[d['offset']:d['offset']+d['length']]))
	value = value.rstrip( '\x00')
	return value

def ExtractUint8(b,d):
	value = b[d['offset']]
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))

def ExtractInt8(b,d):
	value = b[d['offset']]
	if value > 127:
		value = value - 256
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))

def ExtractInt16(b,d):
	value = (b[d['offset']+1]<<8) + b[d['offset']]
	if value > 32767:
		value = value - 65536
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))

def ExtractInt32(b,d):
	value = (b[d['offset']+3]<<24) + (b[d['offset']+2]<<16) + (b[d['offset']+1]<<8) + (b[d['offset']])
	if value > 2147483647:
		value = value - 4294967296
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))
		
def ExtractUint16(b,d):
	value = (b[d['offset']+1]<<8) + b[d['offset']]
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))

def ExtractUint32(b,d):
	value = (b[d['offset']+3]<<24) + (b[d['offset']+2]<<16) + (b[d['offset']+1]<<8) + (b[d['offset']])
	try:
		return int(d['format'].format(value))
	except KeyError:
		return int('{0}'.format(value))
   
def ExtractFloat32(b,d):
	value = struct.unpack('f', b[d['offset']:d['offset']+4])[0]
	return value

def ExtractLEGOVersion(b,d):
	major  = ((b[d['offset']+3] & 0xF0) >> 4 )
	minor  = ((b[d['offset']+3] & 0x0F)	  )
	bugfix = ((b[d['offset']+2]	   )	  )
	build  = ((b[d['offset']+1]	   ) * 100) + (b[d['offset']+0])
	
	return '{0:02}.{1:02}.{2:02}.{3:04}'.format(major,minor,bugfix,build)

def ExtractBluetoothMAC(b,d): 
	a = b[d['offset']:d['offset']+6]
	return '{0:02X}:{1:02X}:{2:02X}:{3:02X}:{4:02X}:{5:02X}'.format(a[0],a[1],a[2],a[3],a[4],a[5])

def ExtractIOTypeID(b,d):
	value = (b[d['offset']+1]<<8) + b[d['offset']]
	try:
		return _ioTypeID_lookup[value]
	except KeyError:
		return 'Unknown IOTypeID: {0}'.format(value)

def generate_uint16(s):
	while True:
		try:
			v = (s[1]<<8) + s[0]
			s = s[2:]
		except IndexError:
			return
		yield v

def ExtractModeCombinations(b,d):
	value = []
	for v in generate_uint16(b[d['offset']:]):
		#print('New Value {}'.format(v))
		value.append(v)
	return value

extractor = { 'string': ExtractString
			, 'uint8':  ExtractUint8
			, 'int8':   ExtractInt8
			, 'LEGOversion': ExtractLEGOVersion
			, 'uint16': ExtractUint16
			, 'uint32': ExtractUint32
			, 'float32': ExtractFloat32
			, 'BluetoothMAC': ExtractBluetoothMAC
			, 'IOTypeID': ExtractIOTypeID
			, 'ModeCombinations': ExtractModeCombinations
			}
			