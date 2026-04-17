
import asyncio
from temporalio.client import Client
import os

async def approve(case_id):
    # client = await Client.connect("localhost:7233")
    client = await Client.connect(
        "ap-south-1.aws.api.temporal.io:7233",
        namespace="puneet-development.fawhu",
        api_key=os.getenv("TEMPORAL_API_KEY"),
        tls=True,
    )
    handle = client.get_workflow_handle(case_id)
    await handle.signal("approve")

if __name__ == "__main__":
    asyncio.run(approve("CASE123"))
