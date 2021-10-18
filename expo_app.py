from flask import Flask, request
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import requests
import uuid
from flask import send_file

#  data of the url of views

dashboard_urls ={
    'promotion': "https://analytics.expo2020.ae//api/3.9/sites/db5b55c4-d2e6-4949-9f9c-7bla46833211/views/c00b8afe-0f89-4b9f-aad4-9c2910830179/image",
    'ticket_sales': "https://analytics.expo2020.ae//api/3.9/sites/db5b55c4-d2e6-4949-9f9c-7bla46833211/views/c00b8afe-0f89-4b9f-aad4-9c2910830179/image",
    'ticket_group': "https://analytics.expo2020.ae//api/3.9/sites/db5b55c4-d2e6-4949-9f9c-7b1a46833211/views/c00b8afe-0f89-4b9f-aad4-9c2910830179/image"

}


maping = {"1": "promotion",
          "2": "ticket_sales",
          "3": "ticket_group"
          }
maping_for_display = {"promotion": "Promotion Performance",
                      "ticket_sales": "Ticket Sales Overview",
                      "ticket_group": "Website Sales"}

# ~ logic of the program starts here

app = Flask(__name__)


@app.route("/")
def hello():
    return "#########"

@app.route("/test")
def hello():
    return "####   test   #####"

@app.route("/get-image/<image_name>")
def get_image(image_name):
    print(image_name)
    #path ='/home/juvanthomas/PycharmProjects/whatsap_tableau/documents/'
    path ='/home/pam.tableau/-------------/-----------/documents/'
    file =path+image_name
    return send_file(path_or_file=file, as_attachment=False)


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')  # whatsap
    # mobile = request.form.get('From')
    query = str(msg)
    try:
        dashboard_name = maping[query]
        keyword = dashboard_urls[maping[query]]
        print(maping[query])
        print('keyword = ', keyword)

        if type(keyword) == str:
            token = log_in()
            HEADERS = {'X-Tableau-Auth': token}
            r = requests.get(url=keyword, headers=HEADERS, verify=False)
            object_name = str(uuid.uuid4())
            folder = "documents/"
            file_to_save = folder + object_name + '.png'
            with open(file_to_save, 'wb') as f:
                f.write(r.content)
                print("Succesfully generated and saved the datasource in Local")

                print("https://analytics.expo2020.ae:8080/get-image/" + object_name+'.png')

            local_url = "https://analytics.expo2020.ae:8080/get-image/" + object_name+'.png'

            print(local_url)

            response = MessagingResponse()
            response.message("Your dashboard is loading ")

            # print(url)

            # Create 1st attachment

            message1 = Message()
            message1.body(maping_for_display[dashboard_name])
            message1.media(local_url)
            response.append(message1)

    except Exception as e:
        print(e)
        response = MessagingResponse()
        response.message(
            "\nBelow are the dashboards available. \nReply with the corresponding number to view it. \n\n 1. Promotion Performance  \n 2. Ticket Sales Overview  \n 3. Website Sales")

    return str(response)


def log_in():
    URL = "https://analytics.expo2020.ae/api/3.6/auth/signin"


    xml = """<tsRequest>
            <credentials name="Tableau.admin" password="@963Password842">
            <site contentUrl="" />
            </credentials>
            </tsRequest>"""

    head = {"Accept": "application/json"}

    r = requests.post(url=URL, data=xml, headers=head, verify=False)
    jsonfile = r.json()
    token = jsonfile["credentials"]["token"]
    return token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
