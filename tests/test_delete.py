def test_delete():
    import requests
    import os
    from dotenv import load_dotenv, find_dotenv
    from pathlib import Path
    import json

    load_dotenv(find_dotenv())

    url=f'{os.environ["URL"]}/delete'
    x = requests.delete(url, json={'key':'README.md'})
    r = json.loads(x.text)
    assert r['ResponseMetadata']['HTTPStatusCode'] == 204