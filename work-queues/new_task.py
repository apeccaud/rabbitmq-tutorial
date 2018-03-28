#!/usr/bin/env python
import sys
import pika

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a queue
# Note: If the queue already exists, it wont create it again
# Good practice to always declare queue in each program using it
channel.queue_declare(queue='task_queue', durable=True)

# Send message
# Using the default exchange -> Allows to specify exactly to which
# queue the message should go
# The queue name has to be specified in the routing_key parameter
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode = 2, # make message persistent by saving it to the disk
    ))
print(" [x] Sent %s" % message)

# Before exiting the program we need to make sure the network buffers 
# were flushed and our message was actually delivered to RabbitMQ
# We can do it by gently closing the connection
connection.close()