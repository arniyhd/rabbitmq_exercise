# RabbitMQ Mobileye exercise

This solution is created out of 2 python scripts and 1 RabbitMQ docker.
This solution only works with a local RabbitMQ container which uses its default ports.


## Start RabbitMQ Docker
`docker run -d --hostname my-rabbit --name rabbit-mq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

## Run the publisher.py file to enter messages
The publisher.py is using Click.cli to get user input for the messages

```
python publisher.py
to_user: Arnold
message: Hey, This is an exercise for Mobileye!
Message Published succesfully
```

## Validate messages in rabbitMQ

You can validate the messages are indeed in the queue by doing docker exec:
`docker exec -it rabbit-mq /bin/bash`

and running `list_queues`:
```bash
root@my-rabbit:/# rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
messages        2
```
## Run the subscriber.py to get the messages

```
python subscriber.py
Subscribe started listening to messages - exit press CTRL+C
Message to david has been logged
Message to arnold has been logged
^CSubsriber have been exited after getting CTRL+C
```

## Open the logs files to validate messages and timestamps

```
cat messages.log
[2023-01-14 11:31:33.661826] To: david Message: david
[2023-01-14 11:31:33.664397] To: arnold Message: Hey, This is an exercise for Mobileye!
```

## Validate messages are no longer in rabbitMQ:

```
docker exec -it rabbit-mq /bin/bash
root@my-rabbit:/# rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
messages        0
```

## Validate a message can't be consumed twice
lets run 2 consumers simultaniously from different paths:

<img width="615" alt="image" src="https://user-images.githubusercontent.com/122671058/212466519-3002d55f-ea9c-438a-bece-5d72bad8e047.png">

as you can see, each subscriber read a unique message.

## Improvements before going to production

Lets say for an example this service goes to production, those are several improvements we can make:

1. Send metrics from the script - either by statsd or prometheus protocol (exposing `/metrics` path) it would be great to have metrics like `messages_published` and `messages recieved` to understand the scale of this service and the utilization of resources (for example - if we needed 1 CPU core for 3000 messages, and now after a deployment we need 1.3 cores for 3000 messages - we downgraded performance) 

2. Allowing connections from non-localhost - this is pretty simple, but add another option to click.cli to choose a non-local rabbitMQ.
This is important for using RabbitMQ Cloud, as it was specified in this exercise (but unfortunatly i dont have an account and couldn't test)
for rabbit cloud usage, we need to implement: 
```
def start_subscriber():
    connection = pika.BlockingConnection(pika.URLParameters('amqp://username:password@rabbitmq-service.com:5672/vhost'))
```

(of course, better to have password saved in a config file, and not as plain text in the code)
