#!/usr/bin/python3
from kafka import KafkaConsumer

topic = input("Topic: ")

consumer = KafkaConsumer(topic, bootstrap_servers=[input("Broker: "])
print("Starting kafka consumer")

print("Metrics: {}".format(consumer.metrics()))
for msg in consumer:
    print("Consumer: {}".format(msg))
