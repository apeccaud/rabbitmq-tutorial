#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare exchange
# 'fanout' is broadcasting all the messages it receives to all the queues it knows
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# Create a random-named queue, which will be deleted when the program stops
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# Bind the created queue to 'logs' exchanger
# Now, every time a message is published to the 'logs' exchanger,
# this message will be forwared to the new queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# Consume messages on the new queue
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()