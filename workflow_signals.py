
import asyncio
from temporalio.client import Client

async def approve(case_id):
    # client = await Client.connect("localhost:7233")
    client = await Client.connect(
        "ap-south-1.aws.api.temporal.io:7233",
        namespace="puneet-development.fawhu",
        api_key="eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ.eyJhY2NvdW50X2lkIjoiZmF3aHUiLCAiYXVkIjpbInRlbXBvcmFsLmlvIl0sICJleHAiOjE4MzkzOTE3MTMsICJpc3MiOiJ0ZW1wb3JhbC5pbyIsICJqdGkiOiJoaWpWeHJ4clc3RTd1akFJNXJ5NWREZ2JkRWNaZ09IRiIsICJrZXlfaWQiOiJoaWpWeHJ4clc3RTd1akFJNXJ5NWREZ2JkRWNaZ09IRiIsICJzdWIiOiJjODNlMjE4NjkzZWY0MDkzYTRjNTE3OWYwZTgzYWM5OSJ9.4E5UYjwf6d49jXf1hOw07o2QN7Jf8du2FXaZf2Yn8qb-RqO3HmecKOeZSS9oH4uKaWaBjsnD64CywBDKL40GDA",
        tls=True,
    )
    handle = client.get_workflow_handle(case_id)
    await handle.signal("approve")

if __name__ == "__main__":
    asyncio.run(approve("CASE123"))
