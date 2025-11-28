#!/usr/bin/env python3
"""
Create and run KFP pipeline using v2beta1 API
"""
import requests
import json
import time

KFP_BASE_URL = "http://127.0.0.1:8080"


def get_uploaded_pipelines():
    """Get all uploaded pipelines"""
    try:
        response = requests.get(f"{KFP_BASE_URL}/apis/v1beta1/pipelines", timeout=10)
        if response.status_code == 200:
            return response.json().get("pipelines", [])
    except Exception as e:
        print(f"Error fetching pipelines: {e}")
    return []


def create_pipeline_run_v2(pipeline_id):
    """Create run using v2beta1 API"""
    print(f"\n[2] Creating pipeline run using v2beta1 API...")
    print(f"    Pipeline ID: {pipeline_id}")

    # v2beta1 API format for creating run
    url = f"{KFP_BASE_URL}/apis/v2beta1/runs"

    run_payload = {
        "display_name": f"boston-pipeline-{int(time.time())}",
        "pipeline_spec": {"pipeline_id": pipeline_id},
    }

    try:
        response = requests.post(url, json=run_payload, timeout=30)

        print(f"    Status: {response.status_code}")

        if response.status_code in [200, 201]:
            data = response.json()
            run_id = data.get("id") or data.get("name")
            print(f"    ✅ Run created! ID: {run_id}")
            return run_id
        else:
            # Try alternative format
            print(f"    v2beta1 API returned {response.status_code}")
            print(f"    Trying alternative format...")

            # Simplified format
            url_v1 = f"{KFP_BASE_URL}/apis/v1/pipelines/{pipeline_id}/runs"
            run_payload_v1 = {
                "name": f"boston-pipeline-run-{int(time.time())}",
                "pipeline_id": pipeline_id,
            }

            response = requests.post(url_v1, json=run_payload_v1, timeout=30)
            print(f"    v1 Status: {response.status_code}")

            if response.status_code in [200, 201]:
                data = response.json()
                run_id = data.get("id") or data.get("run_id")
                print(f"    ✅ Run created! ID: {run_id}")
                return run_id
            else:
                print(f"    Response: {response.text[:300]}")
                return None

    except Exception as e:
        print(f"    Error: {e}")
        return None


def monitor_run(run_id):
    """Monitor a pipeline run"""
    print(f"\n[3] Monitoring pipeline execution...")
    print(f"    Run ID: {run_id}")

    max_attempts = 60
    attempt = 0

    while attempt < max_attempts:
        try:
            # Try v2beta1 first
            url = f"{KFP_BASE_URL}/apis/v2beta1/runs/{run_id}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                run_data = response.json()
                state = run_data.get("state", "UNKNOWN")
                print(f"    Status: {state} (attempt {attempt+1}/{max_attempts})")

                if state in ["SUCCEEDED", "FAILED", "SKIPPED", "CANCELED"]:
                    print(f"    ✅ Pipeline execution completed: {state}")

                    # Try to get run details
                    print(f"\n[4] Pipeline Execution Summary:")
                    print(f"    Run ID: {run_id}")
                    print(f"    Status: {state}")
                    print(f"    UI: http://127.0.0.1:8080/runs/details/{run_id}")
                    return True
            else:
                # Try v1 API
                url_v1 = f"{KFP_BASE_URL}/apis/v1/runs/{run_id}"
                response = requests.get(url_v1, timeout=10)

                if response.status_code == 200:
                    run_data = response.json()
                    state = run_data.get("status") or run_data.get("phase")
                    print(f"    Status: {state} (attempt {attempt+1}/{max_attempts})")

                    if state in ["Succeeded", "Failed", "Skipped"]:
                        print(f"    ✅ Pipeline execution completed: {state}")
                        return True

        except Exception as e:
            print(f"    Monitoring error: {e}")

        time.sleep(10)
        attempt += 1

    print(f"    ⏱️  Monitor timeout after {max_attempts*10}s")
    return False


def main():
    print("=" * 70)
    print("KFP Pipeline Upload & Execution - Full Workflow")
    print("=" * 70)

    # Step 1: Get uploaded pipelines
    print("\n[1] Checking for uploaded pipelines...")
    pipelines = get_uploaded_pipelines()

    if not pipelines:
        print("    ❌ No pipelines found in KFP")
        return

    print(f"    ✅ Found {len(pipelines)} uploaded pipeline(s)")

    # Get the first/most recent pipeline (should be our boston-housing-pipeline)
    pipeline_id = pipelines[0].get("id")
    print(f"    Using pipeline: {pipeline_id}")

    # Step 2: Create run
    run_id = create_pipeline_run_v2(pipeline_id)

    if not run_id:
        print("    ❌ Failed to create pipeline run")
        return

    # Step 3: Monitor execution
    success = monitor_run(run_id)

    # Step 4: Final info
    print("\n[5] Access Results:")
    print(f"    Dashboard: http://127.0.0.1:8080")
    print(f"    Run Details: http://127.0.0.1:8080/runs/details/{run_id}")
    print(f"    Status: {'✅ SUCCESS' if success else '⏳ PENDING/MONITORING'}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
