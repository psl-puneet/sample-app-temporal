from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from datetime import timedelta

# -----------------------
# Activities
# -----------------------

@activity.defn
async def validate_customer(aadhaar: str):
    if len(aadhaar) != 12:
        raise Exception("Invalid Aadhaar")
    return "VALID"

@activity.defn
async def fetch_accounts(aadhaar: str):
    return ["ACC1", "ACC2"]

@activity.defn
async def freeze_funds(data: dict):
    case_id = data["case_id"]
    acc = data["acc"]
    amount = data["amount"]
    print(f"[Freeze] Freezing {amount} in account {acc} for case {case_id}")

@activity.defn
async def unfreeze(data: dict):
    case_id = data["case_id"]
    print(f"[Unfreeze] Releasing funds for case {case_id}")


# -----------------------
# Workflow
# -----------------------

@workflow.defn
class GarnisheeWorkflow:
    def __init__(self):
        self.approved = False
        self.rejected = False
        self.retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=5
        )
    @workflow.run
    async def run(self, case_id: str, aadhaar: str="123455670890", amount: float=40000.6):
        await workflow.execute_activity(validate_customer, aadhaar,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=self.retry_policy)

        accounts = await workflow.execute_activity(fetch_accounts, aadhaar,
            start_to_close_timeout=timedelta(seconds=5))

        for acc in accounts:
            await workflow.execute_activity(
                freeze_funds,
                {"case_id": case_id, "acc": acc, "amount": amount},
                start_to_close_timeout=timedelta(seconds=5)
            )

        # Wait for approval or rejection
        await workflow.wait_condition(
            lambda: self.approved or self.rejected,
            timeout=timedelta(seconds=30)
        )

        # Handle rejection (unfreeze funds)
        if self.rejected:
            await workflow.execute_activity(
                unfreeze,
                {"case_id": case_id},
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=self.retry_policy
            )
    @workflow.signal
    def approve(self):
        self.approved = True
        print("[Signal] Workflow approved")

    @workflow.signal
    def reject(self):
        self.rejected = True
        print("[Signal] Workflow rejected")