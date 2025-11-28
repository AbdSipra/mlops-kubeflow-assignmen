from kfp.client import Client
import json

c = Client(host="http://127.0.0.1:8080")
pipelines = c.list_pipelines()
if pipelines.pipelines:
    p = pipelines.pipelines[-1]
    pid = p.id if hasattr(p, "id") else p.pipeline_id
    print(f"Pipeline ID: {pid}")

    versions = c.list_pipeline_versions(pid)
    print(f"Versions type: {type(versions)}")
    attrs = [x for x in dir(versions) if not x.startswith("_")]
    print(f"Attributes: {attrs}")

    # Try to print as dict
    try:
        print(f"To_dict: {versions.to_dict()}")
    except:
        pass

    # Check each attribute
    for attr in attrs:
        try:
            val = getattr(versions, attr)
            if not callable(val):
                print(f"{attr}: {type(val)}")
                if isinstance(val, list) and val:
                    print(f"  First item: {type(val[0])}")
        except:
            pass
