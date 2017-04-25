import smtplib
from threading import Timer

# TODO: pass email authentication items to file

def intermediate_text(reminder):
    print(reminder)

def text_send(reminder, t):
    '''
    :param reminder: message to remind user of
    :param t: amount of time (in seconds) to wait before sending message
    '''
    tim = Timer(t, intermediate_text, [reminder])
    tim.start()

def intermediate_funct(email, reminder):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login("lgeron@t19s.com", "PorQ1415")
    msg = reminder
    server.sendmail("lgeron@t19s.com", email, msg)


def email_send(email, reminder, t):
    tim = Timer(t, intermediate_funct, [email, reminder])
    tim.start()
