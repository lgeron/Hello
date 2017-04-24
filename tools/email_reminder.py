import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
print("Connecting to server...")
server.ehlo()
server.starttls()

server.login("lgeron@t19s.com", "password123")
print("Connected!")
msg = "Hello!"
server.sendmail("lgeron@t19s.com", "ewilcox@t19s.com", "Hi there")