import faker
import pika

import connect
from models import Contact

fake = faker.Faker()

def seed(n):
    for _ in range(n):
        contact = Contact(fullname=fake.name(), email=fake.email(),
                           number=fake.phone_number(), 
                           favorite=fake.random_choices(['sms', 'email'])[0])
        contact.save()

def main():
    seed(3)
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange='task_email', exchange_type='direct')
    channel.exchange_declare(exchange='task_sms', exchange_type='direct')
    channel.queue_declare(queue='emails', durable=True)
    channel.queue_declare(queue='sms', durable=True)
    channel.queue_bind(exchange='task_email', queue='emails')
    channel.queue_bind(exchange='task_sms', queue='sms')


    contacts = Contact.objects().all()
    for contact in contacts:
        if contact.favorite == 'email' or contact.favorite == None:
            channel.basic_publish(exchange='task_email', routing_key='emails', 
                body=str(contact.id).encode(), 
                properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        elif contact.favorite == 'sms':
            channel.basic_publish(exchange='task_sms', routing_key='sms', 
                body=str(contact.id).encode(),
                properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        
    connection.close()

if __name__ == '__main__':
    main()