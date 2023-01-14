import json
import pika
from pika import exceptions
import click

@click.command()
@click.option('--to_user', prompt='to_user', help='Username of the recipient')
@click.option('--message', prompt='message', help='The Message Body')
@click.option('--publish', default='log', help='Method to publish message')



def publish_message(to_user, message, publish):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    except exceptions.AMQPConnectionError:
        print("you dont have a connection to the local RabbitMQ")
        return(None)

    channel = connection.channel()
    channel.queue_declare(queue='messages')
    message_json = json.dumps({'to_user': to_user, 'message': message, 'publish': publish})
    channel.basic_publish(exchange='', routing_key='messages', body=message_json)
    print("Message Published succesfully")
    connection.close()


if __name__ == '__main__':
    publish_message()
