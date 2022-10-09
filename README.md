# Raspberry Pi 3B/3B+ 2FA

This MVP software provides a cheap, alternate second factor authentication (2FA) phone number on a Raspberry Pi 3B/3B+.  It solves the problem of companies requiring you to add a mobile phone number to your account and then using that phone number for targeting ads, leaking the phone number, etc. Companies keep doing this.  And I don’t see them stopping.

Hacker news discussion that inspired me:
https://news.ycombinator.com/item?id=32399949

## Demo
Below are a couple of screenshots and a short video demo.
Below, the Pi is waiting.
![Screenshot](waiting.png)
And when an SMS comes in it is displayed
![Screenshot](with-messages.png)

The Pi3B is headless and I'm accessing it over VNC.




This MVP only receives SMS.  Voice can be added relatively easily.









I built this for myself and I'm really happy with it.  I want to know if enough people are interested for me to commercialize it.
To cover my costs, I will either charge a small monthly subscription fee or upcharge the twilio usage.  I am not looking to get rich here, just to provide a needed service.

There are some account setup challenges that I need help figuring out.
* Twilio
Twilio uses webhooks.  Setting up Twilio webhooks is error prone.  My original idea was to ask for the Twilio account sid and auth token and do the setup on behalf of the user.  I 
* SIP Signalling


## How to sign up
* Sign up for a free Twilio Account https://www.twilio.com/try-twilio
* Sign up for a free iptel.org sip account https://serweb.iptel.org/user/reg/index.php
* Fill out this form
* Get an email from me with credentials.txt attached
* Flash bullseye on Pi 3B/3B+
