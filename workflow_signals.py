
import asyncio
from temporalio.client import Client

async def approve(case_id):
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(case_id)
    await handle.signal("approve")

if __name__ == "__main__":
    asyncio.run(approve("CASE123"))
