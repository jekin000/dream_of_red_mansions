import json

def generate_send_count(data):
	sendcnts = {}
	for key in data.keys():
		value = data.get(key)
		name = value.split('#')[0] 
		if sendcnts.has_key(name):
			sendcnts[name] = sendcnts[name]+1
		else:
			sendcnts[name] = 1
	return sendcnts
if __name__ == '__main__':
	content = ''
	with open('from_keyvalue.txt','r') as f:	
		content = f.read()

	formated = json.loads(content)
	data = generate_send_count(formated)
	print len(data)
