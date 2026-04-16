
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from garnishee_workflow import *

async def main():
    client = await Client.connect(
        "ap-south-1.aws.api.temporal.io:7233",
        namespace="puneet-development.fawhu",
        api_key="eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ.eyJhY2NvdW50X2lkIjoiZmF3aHUiLCAiYXVkIjpbInRlbXBvcmFsLmlvIl0sICJleHAiOjE4MzkzOTE3MTMsICJpc3MiOiJ0ZW1wb3JhbC5pbyIsICJqdGkiOiJoaWpWeHJ4clc3RTd1akFJNXJ5NWREZ2JkRWNaZ09IRiIsICJrZXlfaWQiOiJoaWpWeHJ4clc3RTd1akFJNXJ5NWREZ2JkRWNaZ09IRiIsICJzdWIiOiJjODNlMjE4NjkzZWY0MDkzYTRjNTE3OWYwZTgzYWM5OSJ9.4E5UYjwf6d49jXf1hOw07o2QN7Jf8du2FXaZf2Yn8qb-RqO3HmecKOeZSS9oH4uKaWaBjsnD64CywBDKL40GDA",
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
