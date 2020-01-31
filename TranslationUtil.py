import requests
import json

class TranslationUtil():
	def __init__(self):
		self.faraazin_header = {"Connection": "keep-alive",\
			 "Accept": "application/json, text/plain, */*", \
			 "Authorization": "Bearer undefined", \
			 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",\
			 "Content-Type": "application/json;charset=UTF-8", \
			 "Origin": "https://www.faraazin.ir", \
			 "Sec-Fetch-Site": "same-origin", \
			 "Sec-Fetch-Mode": "cors",\
			 "Referer": "https://www.faraazin.ir/?q=%D8%AE%D9%88%D8%AF%DA%A9%D8%A7%D8%B1",\
			 "Accept-Encoding": "gzip, deflate, br",\
			 "Accept-Language": "en-US,en;q=0.9",\
			 "Cookie": "_ga=GA1.2.1845074656.1579521051; G_ENABLED_IDPS=google; _mh=%22%2C19%22; _gid=GA1.2.673830774.1579615715; G_AUTHUSER_H=0"\
		}

	def translate(self,word,mode):	#translates a word from farsi to english or vise-versa
		payload = {"text":word,"mode": mode}
		r = requests.post("https://www.faraazin.ir/api/translate", data=json.dumps(payload), headers=self.faraazin_header)
		response = json.loads(r.text)
		return response

	def unify(self, L):	# takes a list and makes its elements unique (e.g. no similars)
		L_copy = []
		for elem in L:
			if elem not in L_copy:
				L_copy.append(elem)
		return L_copy
	
	def clear(self,word):	#removes all non alphanumeric chars from begining and end of str
		fwd_cnt = 0
		while(fwd_cnt < len(word) and word[fwd_cnt].isalnum() == False):
			fwd_cnt += 1
		bwd_cnt = len(word)
		while(bwd_cnt > -1 and word[bwd_cnt - 1].isalnum() == False):
			bwd_cnt-=1

		if bwd_cnt < fwd_cnt:
			return None

		return word[fwd_cnt:bwd_cnt]
