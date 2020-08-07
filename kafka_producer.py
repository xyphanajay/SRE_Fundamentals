#!/usr/bin/python3
from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers=input("Broker: "))
print("Kafka Producer Starting...")
topic = input("Topic:")
i = 0
while True:
    
    print "Server: message: {}".format(i)
    producer.send(topic, 'message: {}'.format(i))
    i += 1
    time.sleep(5)

