import os
from google.cloud import pubsub_v1


class Publisher:
    _topics = ["frame"]

    def __init__(self):
        self.client = pubsub_v1.PublisherClient()
        self.createTopics()

    def createTopics(self):
        for topic in self._topics:
            self.client.create_topic(name=self.buildTopic(topic))

    def buildTopic(topic: str) -> str:
        return "projects/{project_id}/topics/{topic}".format(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
            topic=topic,
        )

    async def publish(self, topic_name: str, data: str):
        return await self.client.publish(self.buildTopic(topic_name), data)

    async def initialize(self, topic: str):
        await self.publish(topic, b"Initialized!", spam="eggs")
