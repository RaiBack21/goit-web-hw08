import pika
import sys

import connect
from models import Contact

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials
    ))
    channel = connection.channel()

    channel.queue_declare(queue='sms', durable=True)


    def callback(ch, method, properties, body):
        print("Send sms")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        contact = Contact.objects(id=body.decode()).first()
        contact.update(set__is_sent=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms', on_message_callback=callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0) 
        