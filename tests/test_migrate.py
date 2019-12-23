def test_migrate():
    import requests
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

    url=f'{os.environ['URL']}/migrate'
    EDM_DATA=os.environ['EDM_DATA']
    RECIPE=os.environ['RECIPE_ENGINE']
    x = requests.post(url, json = 
                    {"src_engine": f"{RECIPE}",
                    "dst_engine": f"{EDM_DATA}",
                    "src_schema_name": "test",
                    "dst_schema_name": "test",
                    "src_version": "latest",
                    "dst_version": "latest"})
    assert x.text['status'] == 'success'