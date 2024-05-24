from fastapi import FastAPI, HTTPException
from kubernetes import client, config
import os
import datetime

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    kubeconfig_path = os.getenv("KUBECONFIG_PATH", "~/.kube/config")
    config.load_kube_config(config_file=kubeconfig_path)

@app.post("/trigger-job/")
async def trigger_job(name: str):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    
    # Generate a unique job name
    job_name = f"dummy-job-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Define the job specification with TTL
    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            ttl_seconds_after_finished=30,  # Set TTL to 30 seconds
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="dummy",
                            image="busybox",
                            command=["/bin/sh", "-c", f"echo Hello {name}"]
                        )
                    ],
                    restart_policy="Never"
                )
            )
        )
    )

    # Create the job in the default namespace
    batch_v1 = client.BatchV1Api()
    batch_v1.create_namespaced_job(namespace="default", body=job)

    return {"message": f"Job {job_name} triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
  
