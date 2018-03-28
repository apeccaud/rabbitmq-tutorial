#!/usr/bin/env python
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a queue
# Note: If the queue already exists, it wont create it again
# Good practice to always declare queue in each program using it
# A durable queue will be preserved even after RabbitMq restarts
channel.queue_declare(queue='task_queue', durable=True)

# Callback function is called whenever the consumer receives a message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Send acknowledgment once the task is done
    # Ensures that the message will be processed, even if the current
    # worker dies (redistributed)
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Don't dispatch a new message to a worker until it has processed and acknowledged the previous one
channel.basic_qos(prefetch_count=1)

# Create the consumer
# no_ack parameter disables the default acknowledgment policy (not recommended)
channel.basic_consume(callback,
    queue='task_queue')

# Enter a never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
