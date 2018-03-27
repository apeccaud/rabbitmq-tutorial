#!/usr/bin/env python
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a queue
# Note: If the queue already exists, it wont create it again
# Good practice to always declare queue in each program using it
channel.queue_declare(queue='hello')

# Callback function is called whenever the consumer receives a message
def callback(ch, method, properties, body):
    print(" [x] Received %r " % body)

# Create the consumer
# no_ack parameter disables the default acknowledgment policy (not recommended)
channel.basic_consume(callback,
    queue='hello',
    no_ack=True)

# Enter a never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
