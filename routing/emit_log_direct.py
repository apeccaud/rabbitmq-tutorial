#!/usr/bin/env python
import sys
import pika

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange
# "direct" only forward messages to queues that are binded to a specific routing key
channel.exchange_declare(exchange="direct_logs",
                         exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange="direct_logs",
                      routing_key=severity,
                      body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()
