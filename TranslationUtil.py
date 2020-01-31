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