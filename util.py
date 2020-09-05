import requests as r
from zipfile import ZipFile
import io

def unpack_zip(url, zipname, path=None):
	"""
	1) write zip file to temp disk
	2) unzip, and rewrite permanently 
	3) delete temp zip
	4) return dict of cal, lab, pre, and def
	"""
	
	# fetch url, convert to bytes, unzip, then extract
	response = r.get(url + zipname)
	response = io.BytesIO(response.content)
	f = ZipFile(response, 'r')
	f.extractall(path=path)
	namelist = f.namelist()
	f.close() # remember to close the zip!
	
	namedict = {
		"calculationLink": None,
		"definitionLink": None,
		"labelLink": None,
		"presentationLink": None,
		"misc": []
		}

	for name in namelist:
		if name[-7:-4] == 'cal':
			namedict["calculationLink"] = name
		elif name[-7:-4] == 'def':
			namedict["definitionLink"] = name
		elif name[-7:-4] == 'lab':
			namedict["labelLink"] = name
		elif name[-7:-4] == 'pre':
			namedict["presentationLink"] = name
		else:
			namedict["misc"].append(name)

	return namedict
