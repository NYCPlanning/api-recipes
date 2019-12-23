def test_upload():
    import requests
    import os
    from dotenv import load_dotenv, find_dotenv
    from pathlib import Path
    import json

    load_dotenv(find_dotenv())

    url=f'{os.environ["URL"]}/upload'
    files={'file': open(Path(__file__).parent.parent/'README.md','rb')}
    x = requests.post(url, files=files, json={'key':'README.md', 'acl':'private'})
    r = json.loads(x.text)
    assert r['ResponseMetadata']['HTTPStatusCode'] == 200

test_upload()