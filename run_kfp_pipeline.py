#!/usr/bin/env python3
"""
Create and run a KFP pipeline
"""
import requests
import json
import time
import subprocess

KFP_BASE_URL = "http://127.0.0.1:8080"


def get_pipelines():
    """List all pipelines"""
    try:
        response = requests.get(f"{KFP_BASE_URL}/apis/v1beta1/pipelines", timeout=10)
        if response.status_code == 200:
            data = response.json()
            pipelines = data.get("pipelines", [])
            return pipelines
    except:
        pass
    return []


def create_run_from_yaml():
    """Create and run pipeline using kubectl directly"""
    print("=" * 60)
    print("KFP Pipeline Execution via Kubernetes")
    print("=" * 60)

    # Create a run using kfp CLI through Kubernetes
    print("\n[1] Creating pipeline run...")

    run_config = {
        "apiVersion": "kubeflow.org/v1beta1",
        "kind": "PipelineRun",
        "metadata": {"name": "boston-housing-run", "namespace": "kubeflow"},
        "spec": {"pipelineRef": {"name": "pipeline.yaml"}},
    }

    # Try to submit pipeline directly
    try:
        result = subprocess.run(
            [
                "minikube",
                "kubectl",
                "--",
                "apply",
                "-f",
                "pipeline.yaml",
                "-n",
                "kubeflow",
            ],
            cwd="c:\\Users\\abdul\\Desktop\\mlops-kubeflow-assignmen",
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print(f"    ✅ Pipeline applied successfully")
        else:
            print(f"    Output: {result.stdout}")
            print(f"    Error: {result.stderr}")

    except Exception as e:
        print(f"    Error: {e}")

    # List existing pipelines
    print("\n[2] Querying existing pipelines in KFP...")
    pipelines = get_pipelines()

    if pipelines:
        print(f"    Found {len(pipelines)} pipeline(s):")
        for i, pipeline in enumerate(pipelines, 1):
            print(
                f"      {i}. {pipeline.get('display_name', 'N/A')} (ID: {pipeline.get('id')})"
            )

            # Try to create a run from the first pipeline
            if i == 1:
                pipeline_id = pipeline.get("id")
                print(f"\n[3] Creating run from pipeline: {pipeline_id}")

                # Create run with v2beta1 API
                run_body = {
                    "display_name": f"boston-housing-run-{int(time.time())}",
                    "pipeline_spec": {"pipeline_id": pipeline_id},
                }

                try:
                    response = requests.post(
                        f"{KFP_BASE_URL}/apis/v1beta1/runs", json=run_body, timeout=30
                    )

                    if response.status_code in [200, 201]:
                        run_data = response.json()
                        run_id = run_data.get("id")
                        print(f"    ✅ Run created! ID: {run_id}")

                        # Monitor execution
                        print(f"\n[4] Monitoring execution...")
                        monitor_run(run_id)

                    else:
                        print(f"    Status: {response.status_code}")
                        print(f"    Response: {response.text[:500]}")

                except Exception as e:
                    print(f"    Error creating run: {e}")
    else:
        print("    No pipelines found. Uploading pipeline.yaml first...")
        upload_and_run()


def upload_and_run():
    """Upload pipeline and create run"""
    print("\n[2b] Uploading pipeline.yaml...")

    try:
        with open("pipeline.yaml", "rb") as f:
            files = {"uploadfile": f}
            response = requests.post(
                f"{KFP_BASE_URL}/apis/v1beta1/pipelines/upload", files=files, timeout=30
            )

        if response.status_code == 200:
            pipeline_data = response.json()
            pipeline_id = pipeline_data.get("id")
            print(f"    ✅ Uploaded! ID: {pipeline_id}")

            # Create run
            print(f"\n[3] Creating run...")
            run_body = {
                "display_name": f"boston-housing-run-{int(time.time())}",
                "pipeline_spec": {"pipeline_id": pipeline_id},
            }

            response = requests.post(
                f"{KFP_BASE_URL}/apis/v1beta1/runs", json=run_body, timeout=30
            )

            if response.status_code in [200, 201]:
                run_data = response.json()
                run_id = run_data.get("id")
                print(f"    ✅ Run created! ID: {run_id}")

                # Monitor
                print(f"\n[4] Monitoring execution...")
                monitor_run(run_id)
            else:
                print(f"    Failed: {response.status_code}")
                print(f"    {response.text[:500]}")
        else:
            print(f"    Failed: {response.status_code}")
            print(f"    {response.text[:500]}")

    except Exception as e:
        print(f"    Error: {e}")


def monitor_run(run_id):
    """Monitor a pipeline run"""
    max_wait = 600  # 10 minutes
    check_interval = 10
    elapsed = 0

    while elapsed < max_wait:
        try:
            response = requests.get(
                f"{KFP_BASE_URL}/apis/v1beta1/runs/{run_id}", timeout=10
            )

            if response.status_code == 200:
                run_data = response.json()
                state = run_data.get("state", "UNKNOWN")

                print(f"    Status: {state} (elapsed: {elapsed}s)")

                if state in ["SUCCEEDED", "FAILED", "SKIPPED", "CANCELED"]:
                    if state == "SUCCEEDED":
                        print(f"    ✅ Pipeline completed successfully!")
                    else:
                        print(f"    ⚠️  Pipeline ended with status: {state}")
                    break
        except:
            pass

        time.sleep(check_interval)
        elapsed += check_interval

    if elapsed >= max_wait:
        print(f"    ⏱️  Timeout reached ({max_wait}s)")

    print(f"\n[5] Access KFP UI:")
    print(f"    Dashboard: http://127.0.0.1:8080")
    print(f"    Run: http://127.0.0.1:8080/runs/details/{run_id}")


if __name__ == "__main__":
    create_run_from_yaml()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
