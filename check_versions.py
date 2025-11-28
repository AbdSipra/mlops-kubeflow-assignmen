from kfp.client import Client

c = Client(host="http://127.0.0.1:8080")
try:
    pipelines = c.list_pipelines()
    if pipelines.pipelines:
        p = pipelines.pipelines[-1]
        pid = p.id if hasattr(p, "id") else p.pipeline_id
        print(f"Pipeline ID: {pid}")

        versions = c.list_pipeline_versions(pid)
        print(f"Versions response: {versions}")
        if hasattr(versions, "versions") and versions.versions:
            v = versions.versions[0]
            vid = v.id if hasattr(v, "id") else v.pipeline_version_id
            print(f"Version ID: {vid}")
        else:
            print("No versions found")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
