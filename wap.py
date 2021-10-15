from flask import Flask, request
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import requests
import uuid

# ~ data of the url of views
dashboard_urls = {
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


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')  # whatsap
    # msg = request.json["text"]              #postman

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
            r = requests.get(url=keyword, headers=HEADERS,verify=False)
            object_name = str(uuid.uuid4())
            folder = "documents/"
            file_to_save = folder + object_name + '.png'
            with open(file_to_save, 'wb') as f:
                f.write(r.content)
                print("Succesfully generated and saved the datasource in Local")
                print("https://analytics.expo2020.ae/" + file_to_save)
            local_url = "https://analytics.expo2020.ae/" + file_to_save
            print(local_url)
            # uploader('whatsapp-doc', keyword, r.content)
            # url=create_presigned_url('whatsapp-doc',keyword)
            response = MessagingResponse()
            response.message("Your dashboard is loading ")

            # print(url)

            # Create 1st attachment

            message1 = Message()
            message1.body(maping_for_display[dashboard_name])
            message1.media(local_url)
            response.append(message1)

            # #Create 2nd attacment

            # message2 = Message()
            # message2.body('Dashboard')
            # message2.media('https://whatsapp-doc.s3.ap-south-1.amazonaws.com/performance.pdf')
            # response.append(message2)

    except Exception as e:
        print(e)
        #        response = MessagingResponse()
        #        response.message("Sorry I did not understand ")
        response = MessagingResponse()
        response.message(
            "\nBelow are the dashboards available. \nReply with the corresponding number to view it. \n\n 1. Promotion Performance  \n 2. Ticket Sales Overview  \n 3. Website Sales")

    return str(response)


def create_presigned_url(bucket_name, object_name, expiration=100):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    ACCESS_KEY_ID = 'AKIAX3ZYFGDONLWJLHWY'
    ACCESS_SECRET_KEY = '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'
    # BUCKET_NAME = 'whatsapp-doc'
    # FILE_NAME = 'forecast.pdf'

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY,
                             config=Config(signature_version='s3v4', region_name='ap-south-1'))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def uploader(bucket_name, object_name, data):
    ACCESS_KEY_ID = 'AKIAX3ZYFGDONLWJLHWY'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = bucket_name
    FILE_NAME = object_name

    data = data

    # S3 Connect
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4'),
    )

    # Image Uploaded
    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ContentType='image/png')
    print('data uploaded')


def log_in():
    import requests

    ##########

    ##########
    URL = "https://analytics.expo2020.ae/api/3.6/auth/signin"
    # URL = "https://ask.beinex.com/api/3.6/auth/signin"
    # URL = "http://10.0.255.1:8080/api/3.6/auth/signin"         # : use 10.0.255.1  for Beinex5Ghz

    xml = """<tsRequest>
            <credentials name="Tableau.admin" password="@963Password842">
            <site contentUrl="" />
            </credentials>
            </tsRequest>"""

    head = {"Accept": "application/json"}

    r = requests.post(url=URL, data=xml, headers=head,verify=False)

    jsonfile = r.json()
    token = jsonfile["credentials"]["token"]

    return token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
