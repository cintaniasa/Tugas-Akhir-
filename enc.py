import json

kunci = "202410102089_202410103012"
def xor(bytearr):
	pos = 0
	bytearr = list(bytearr)
	for i in range(len(bytearr)):
		bytearr[i] = bytearr[i] ^ ord(kunci[pos])
		pos = (pos + 1) % len(kunci)
	bytearr = bytes(bytearr)
	return bytearr

#open with enc
def openJSON_as_dict(filename):
    with open(filename, 'rb') as f:
    	return eval(xor(f.read()).decode('utf-8'))

#write with enc
def writeJSON(data, filename):
	with open(filename, 'wb') as f:
		e = str(data).encode('utf-8')
		f.write(xor(e))

#open without enc
def openNormal(filename):
	with open(filename, 'r') as f:
		return json.load(f)