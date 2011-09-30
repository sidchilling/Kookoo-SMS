'''This is the library which can be used for sending SMS using Kookoo.
'''

domain = 'www.kookoo.in'
api_key = 'XXXXXXXXXXXXXXXXXXXXXX' #Replace this by your api_key
max_message_length = 150 #Replace this by the length by which you want to restrict the message.
                         #Please note the length is restricted by the telecom provider



class MessageLengthExceededException(Exception):
    '''This exception is raised when the message length is more than the one configured
    '''
    pass

class KookooSendSMSException(Exception):
    '''This exception is raised when the SMS sending encountered an exception from Kookoo
    '''
    def __init__(self, message):
	Exception.__init__(self, message)


def send_kookoo_sms(phone_no = None, message = None):
    '''This method sends a swms using Kookoo. Raises Exception if SMS not successfully sent
    '''
    assert phone_no, 'Phone number cannot be None'
    assert message, 'Message cannot be None'
    if len(message) > max_message_length:
	raise MessageLengthExceededException()
    try:
	import requests
	from xml.dom import minidom
    except:
	print 'Required packages: requests (the one from twitter), xml.doc'
	exit()
    params = {}
    params['message'] = message
    params['phone_no'] = phone_no
    params['api_key'] = api_key
    url = 'http://www.kookoo.in/outbound/outbound_sms.php'
    try:
	response = requests.get(url = url, params = params)
	http_response = minidom.parseString(response.content)
	status = http_response.getElementsByTagName('status')
	if status is not None and status.length != 0:
	    status = status[0]
	    if 'success' not in status.toxml():
		raise KookooSendSMSException(http_response.getElementsByTagName('message')[0].toxml())
    except Exception as e:
	print e
	raise Exception()


if __name__ == '__main__':
    #sends a test sms to the number mentioned. Replace the number with the number you want to send SMS to
    #The number must be 10 digit like 9861098610. No need to add +91 in the beginning
    send_kookoo_sms(phone_no = '0000000000', message = 'This is an inbuilt test message from the Python library')