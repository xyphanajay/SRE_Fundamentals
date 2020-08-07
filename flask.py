import confluent_kafka as ck
import confluent_kafka.admin as ckAdmin
import zc.zk
import time

producer = None
adminClient = None
zkClient = None
consumer = None

def init(config):
	create_admin_client(config["adminClient"])
	create_zookeeper_client(config["zookeeperClient"])

def create_producer(config):
	global producer
	producer = ck.Producer(**config)

def create_admin_client(config):
	global adminClient
	adminClient = ckAdmin.AdminClient(config)

def create_zookeeper_client(config):
	global zkClient
	zkClient = zc.zk.ZooKeeper(**config)

def create_consumer(config):
	global consumer
	consumer = ck.Consumer(**config)

def delete_topic(topics):
	if len(topics) == 0:
		return
	print(topics)
	print(adminClient.list_topics().topics)
	fs = adminClient.delete_topics(topics)
	exceptions = []

	for topic, f in fs.items():
		try:
			f.result()
			print("Topic {} deleted".format(topic,operation_timeout=50))
		except Exception as e:
			exceptions.append("Failed to delete topic {} : {}".format(topic, e))

	if len(exceptions) != 0:
		raise Exception(''.join(x for x in exceptions))
	#for topic in topics:

		#zkClient.    delete_recursive("brokers/topics/" + topic)

def create_topic(topics):
	availableTopics = adminClient.list_topics().topics
	topicsToDelete = []

	for topic in topics:
		if topic in availableTopics:
			topicsToDelete.append(topic)

	delete_topic(topicsToDelete)
	time.sleep(0.1)
	newTopics = []
	for topic in topics:
		newTopics.append(ckAdmin.NewTopic(topic, 1, 1))

	fs = adminClient.create_topics(newTopics)
	print(fs)
	exceptions = []
	for topic, f in fs.items():
		try:
			f.result()
			print("Topic {} created".format(topic))
		except Exception as e:
			exceptions.append("Failed to create topic {} : {}".format(topic, e))

	if len(exceptions) != 0:
		raise Exception(''.join(x for x in exceptions))


def send_message(topic, message):
	topics = adminClient.list_topics().topics
	if topic not in topics:
		raise Exception("Topic {} not found".format(topic))
	producer.produce(topic, message)
	producer.flush()

def read_messages(topic, timeout=10):
	availableTopics = adminClient.list_topics().topics

	if topic not in availableTopics:
		raise Exception("Topic {} not found". format(topic))

	topicPartitions = []

	for partition in availableTopics[topic].partitions.keys():
		topicPartitions.append(ck.TopicPartition(topic, partition, ck.OFFSET_BEGINNING))

	consumer.assign(topicPartitions)

	messages = []

	while True:
		msg = consumer.poll(timeout=timeout)
		if not msg or msg.error():
			break
		messages.append(msg.value())

	return messages

def close_consumer():
	consumer.close()
