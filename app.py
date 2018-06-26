import sendgrid
from sendgrid.helpers.mail import *
import time
import requests
import os
from datetime import datetime


def send_mail(cont):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("amitcoh@bynet.co.il")
    to_email = Email("cohen.amitc@gmail.com")
    subject = "Tomorrowland bracelet status changed!"
    content = Content("text/plain", cont)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response


def main():
    res = requests.get("https://track.bpost.be/btr/api/items?itemIdentifier=FW27SGEIY")
    events = None
    events_len = 0
    content = None
    while True:
        try:
            if res.status_code == 200:
                res_json = res.json()
                events = res_json['items'][0]['events']
                if len(events) > events_len:
                    events_len = len(events)
                    content = "There are {} events!\n\n".format(events_len)
                    for event in events:
                        content += "%{} {}: Key: {} Location: {}".format(
                            event['time'], event['date'], event['key'], event['location']['en']
                        )
                        content += "\n\n"
                    my_email = send_mail(content)
                    print my_email.status_code
                    print my_email.body
                    print my_email.headers
                    print content
                else:
                    print "%{}: No changes found!".format(datetime.now())
            time.sleep(60)
        except KeyboardInterrupt:
            ans = str(raw_input("Are you sure you want to stop? [Y/N]"))
            while ans[0].lower() != 'y' or ans[0].lower() != 'n':
                print "Wrong input!"
                ans = str(raw_input("Are you sure you want to stop? [Y/N]"))
            if ans[0].lower() == 'y':
                break
            elif ans[0].lower() == 'n':
                continue


if __name__ == "__main__":
    print "Started application at {}".format(datetime.now())
    main()
    print "Application terminated by user."
