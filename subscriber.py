import json
import pika
import datetime


def handle_message(channel, method, properties, body):
    message = json.loads(body)
    if 'to_user' in message and 'message' in message and 'publish' in message:
        if message['publish'] == 'log':
            with open('messages.log', 'a') as log_file:
                log_file.write(f'[{datetime.datetime.now()}] To: {message["to_user"]} Message: {message["message"]}\n')
            print(f'Message to {message["to_user"]} has been logged')
            channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Invalid message!")


def start_subscriber():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='messages')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='messages', on_message_callback=handle_message)
    print('Subscriber started listening to messages - exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
        print("Subsriber have been exited after getting CTRL+C")

if __name__ == '__main__':
    start_subscriber()
