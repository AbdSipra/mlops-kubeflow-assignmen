#!/usr/bin/env python3
"""
Upload compiled pipeline.yaml to KFP UI and run it
"""
import requests
import json
import time
import sys

# KFP API endpoints
KFP_BASE_URL = "http://127.0.0.1:8080"
UPLOAD_URL = f"{KFP_BASE_URL}/apis/v1beta1/pipelines/upload"
CREATE_RUN_URL = f"{KFP_BASE_URL}/apis/v1beta1/runs"
LIST_PIPELINES_URL = f"{KFP_BASE_URL}/apis/v1beta1/pipelines"


def upload_pipeline(pipeline_file):
    """Upload pipeline YAML to KFP"""
    print(f"[1] Uploading pipeline: {pipeline_file}")

    try:
        with open(pipeline_file, "rb") as f:
            files = {"uploadfile": f}
            response = requests.post(UPLOAD_URL, files=files, timeout=30)

        print(f"    Status: {response.status_code}")

        if response.status_code in [200, 201]:
            pipeline_data = response.json()
            pipeline_id = pipeline_data.get("id")
            pipeline_name = pipeline_data.get("name")
            print(f"    ✅ Success! Pipeline ID: {pipeline_id}")
            print(f"    Pipeline Name: {pipeline_name}")
            return pipeline_id, pipeline_name
        else:
            print(f"    ❌ Failed: {response.text}")
            return None, None

    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None, None


def create_run(pipeline_id, run_name):
    """Create and run a pipeline in KFP"""
    print(f"\n[2] Creating run for pipeline: {pipeline_id}")

    run_body = {
        "display_name": run_name,
        "pipeline_spec_binding": {"pipeline_id": pipeline_id},
    }

    try:
        response = requests.post(CREATE_RUN_URL, json=run_body, timeout=30)
        print(f"    Status: {response.status_code}")

        if response.status_code in [200, 201]:
            run_data = response.json()
            run_id = run_data.get("id")
            print(f"    ✅ Run created! Run ID: {run_id}")
            return run_id
        else:
            print(f"    ❌ Failed: {response.text}")
            return None

    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None


def get_run_status(run_id):
    """Get the status of a pipeline run"""
    try:
        response = requests.get(f"{CREATE_RUN_URL}/{run_id}", timeout=10)
        if response.status_code == 200:
            run_data = response.json()
            return run_data.get("state"), run_data.get("display_name")
        return None, None
    except:
        return None, None


def main():
    pipeline_file = "pipeline.yaml"

    print("=" * 60)
    print("KFP Pipeline Upload & Execution")
    print("=" * 60)

    # Step 1: Upload pipeline
    pipeline_id, pipeline_name = upload_pipeline(pipeline_file)

    if not pipeline_id:
        print("\n❌ Failed to upload pipeline. Exiting.")
        sys.exit(1)

    # Step 2: Create and run
    run_id = create_run(pipeline_id, f"run-{int(time.time())}")

    if not run_id:
        print("\n❌ Failed to create run. Exiting.")
        sys.exit(1)

    # Step 3: Monitor execution
    print(f"\n[3] Monitoring run execution...")
    print(f"    Run ID: {run_id}")

    max_wait = 300  # 5 minutes
    check_interval = 5
    elapsed = 0

    while elapsed < max_wait:
        state, name = get_run_status(run_id)

        if state:
            print(f"    Status: {state}")

            if state in ["SUCCEEDED", "FAILED", "SKIPPED", "CANCELED"]:
                if state == "SUCCEEDED":
                    print(f"    ✅ Pipeline execution completed successfully!")
                else:
                    print(f"    ⚠️  Pipeline execution ended with status: {state}")
                break

        time.sleep(check_interval)
        elapsed += check_interval
        print(f"    Waiting... ({elapsed}s/{max_wait}s)")

    if elapsed >= max_wait:
        print(f"    ⚠️  Timeout reached. Run may still be executing.")

    # Step 4: Provide UI link
    print(f"\n[4] Access KFP UI:")
    print(f"    UI: http://127.0.0.1:8080")
    print(f"    Run: http://127.0.0.1:8080/runs/details/{run_id}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
