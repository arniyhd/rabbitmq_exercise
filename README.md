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
Message to arnold has been logged
Message to Arnold has been logged
^CSubsriber have been exited after getting CTRL+C
```

## Open the logs files to validate messages and timestamps

```
cat messages.log
[2023-01-14 11:31:33.661826] To: david Message: david
[2023-01-14 11:31:33.664397] To: Arnold Message: Hey, This is an exercise for Mobileye!
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

