import smtplib
from threading import Timer

# TODO: pass email authentication items to file

def intermediate_text(reminder):
    print(reminder)

def text_send(reminder, t):
    #TODO: take time t in as format 2017-05-24T00:00:00.000-07:00 and be able to process it
    '''
    :param reminder: message to remind user of
    :param t: amount of time (in seconds) to wait before sending message
    '''
    tim = Timer(t, intermediate_text, [reminder])
    tim.start()

def intermediate_funct(to_email, reminder):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    from_email = 'your email'
    pwd = 'your password'

    server.login(from_email, pwd)
    msg = reminder
    server.sendmail(from_email, to_email, msg)


def email_send(email, reminder, t):
    tim = Timer(t, intermediate_funct, [email, reminder])
    tim.start()
