
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from garnishee_workflow import *

async def main():
    client = await Client.connect(
        "ap-south-1.aws.api.temporal.io:7233",
        namespace="puneet-development.fawhu",
        api_key=os.getenv("TEMPORAL_API_KEY"),
        tls=True,
    )
    worker = Worker(
        client,
        task_queue="garnishee-task-queue",
        workflows=[GarnisheeWorkflow],
        activities=[validate_customer, fetch_accounts, freeze_funds, unfreeze],
    )
    print("Worker started...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
