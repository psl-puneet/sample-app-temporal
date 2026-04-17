
from fastapi import FastAPI
import os
from temporalio.client import Client
from garnishee_workflow import GarnisheeWorkflow

app = FastAPI()

@app.post("/start")
async def start(case_id: str, aadhaar: str, amount: float):
    client = await Client.connect(
        "ap-south-1.aws.api.temporal.io:7233",
        namespace="puneet-development.fawhu",
        api_key=os.getenv("TEMPORAL_API_KEY"),
        tls=True,
    )
    handle = await client.start_workflow(
        GarnisheeWorkflow,
        {
        "case_id":case_id,
        "aadhaar":aadhaar, 
        "amount":amount,
        },
        id=case_id,
        task_queue="garnishee-task-queue",
    )
    return {"workflow_id": handle.id}
