def test_archive():
    import requests
    import os

    url=os.environ['URL']

    x = requests.post(url, json = {"dstSRS": "EPSG:4326",
                                    "srcSRS": "EPSG:4326",
                                    "schema_name": "test",
                                    "version_name": "",
                                    "geometryType": "MULTIPOLYGON",
                                    "layerCreationOptions": [
                                        "OVERWRITE=YES",
                                        "PRECISION=NO"
                                    ],
                                    "metaInfo": "NYC Opendata",
                                    "path": "https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON",
                                    "srcOpenOptions": [],
                                    "newFieldNames": []
                                })
    assert x.text['status'] == 'success'