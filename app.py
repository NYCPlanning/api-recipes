import os
from flask import Flask, request, jsonify
import json
from utils.s3 import make_client, bucket
from utils.etl import engine, ftp_prefix, migrate_table
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from cook import Archiver
import pandas as pd

app = Flask(__name__)
client = make_client()

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    uploading file to s3
    """
    file = request.files['file']
    config = request.form
    key = config.get('key', file.filename)
    acl = config.get('acl', 'private')
    response = client.put_object(
        ACL=acl,
        Body=file.read(),
        Bucket=bucket,
        Key=key)
    return jsonify(response)

@app.route('/delete', methods=['DELETE'])
def delete_file():
    """
    deleting file from s3
    """
    config=request.get_json()
    key=config['key']
    response = client.delete_object(
        Bucket=bucket,
        Key=key)
    return jsonify(response)

@app.route('/archive', methods=['POST'])
def archive():
    config=request.get_json()
    archiver = Archiver(engine=engine, ftp_prefix=ftp_prefix)
    con = create_engine(engine)
    schema_name = config['schema_name']
    try:
        archiver.archive_table(config)
        con.execute(f'''DELETE FROM meta.json_recipes 
                        WHERE schema_name = '{schema_name}';
                    ''')
        con.execute(f'''INSERT INTO meta.json_recipes (schema_name, config) 
                        VALUES ('{schema_name}', '{json.dumps(config)}')
                    ''')
        return jsonify({
            'status': 'success', 
            'schema_name': schema_name, 
        })
    except:
        return jsonify({
            'status': 'failure', 
            'schema_name': schema_name, 
        })

@app.route('/migrate', methods=['POST'])
def migrate():
    """
    migrate table from database A to B
    table_name.version in A 
    to table_name.version in B
    """
    config=request.get_json()
    try:
        migrate_table(**config)
        return jsonify({
            'status': 'success', 
            'schema_name': config, 
        })
    except: 
        return jsonify({
            'status': 'failure', 
            'schema_name': config, 
        })

# @app.route('/download', methods=['GET'])
# def download():
#     """
#     download file from given database to 
#     different format using gdal, 
#     including csv, shapfiles, geojson
#     """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)