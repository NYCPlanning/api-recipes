def test_import():
    import requests
    import os
    from dotenv import load_dotenv, find_dotenv
    import json 
    load_dotenv(find_dotenv())

    url=f'{os.environ["URL"]}/import'
    EDM_DATA=os.environ['EDM_DATA']
    RECIPE=os.environ['RECIPE_ENGINE']
    x = requests.post(url, json = 
                    {"recipe_engine": f"{RECIPE}",
                    "build_engine": f"{EDM_DATA}",
                    "schema_name":"test"})
    r = json.loads(x.text)
    assert r['status'] == 'success'