# downloading tableau datasource to local
import requests
import time

URL = "http://61.2.141.81:8080/api/3.6/auth/signin"
#URL = "http://10.0.255.1:8080/api/3.6/auth/signin"         # : use 10.0.255.1  for Beinex5Ghz



xml = """<tsRequest>
	    <credentials name="beinexadmin" password="Bein3x@987">
		<site contentUrl="" />
	    </credentials>
        </tsRequest>"""

head = {"Accept": "application/json"}

r = requests.post(url=URL, data=xml, headers=head)

jsonfile = r.json()
token = jsonfile["credentials"]["token"]
print(token)
URL= 'http://61.2.141.81:8080//api/3.6/sites/3dccc5ce-a7e1-498f-a3d6-816927b960cd/views/edd436a9-25db-40d9-afba-fb9eb2f2a5d3/data'
# URL = "http://61.2.141.81:8080//api/3.6/sites/3dccc5ce-a7e1-498f-a3d6-816927b960cd/views/87159628-d81b-4d39-8624-977af6167ab2/pdf"

print(URL)
HEADERS = {'X-Tableau-Auth':token}

re = requests.get(url=URL,headers=HEADERS)
print(re.text)

# file_to_save = 'dox1.pdf'
# with open(file_to_save, 'wb') as f:
#     f.write(re.content)
#     print("Succesfully generated and saved the datasource in Local")
