import os
import json
from flask import Flask, request, jsonify
from utils.s3 import make_client, bucket
from utils.etl import engine, ftp_prefix, migrate_table
from sqlalchemy import create_engine
from cook import Archiver, Importer
import pandas as pd

app = Flask(__name__)
client = make_client()

@app.route('/', methods=['GET'])
def welcome(): 
    return jsonify('welcome!!!!!!')

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
    schema_name=config.get('schema_name')
    try:
        migrate_table(**config)
        config.pop('src_engine')
        config.pop('dst_engine')
        return jsonify({
            'status': 'success', 
            'config': config, 
        })
    except:
        config.pop('src_engine')
        config.pop('dst_engine')
        return jsonify({
            'status': 'failure', 
            'config': config, 
        })

@app.route('/import', methods=['POST'])
def importing():
    """
    import table from database A to B
    may considering merging this endpoint
    with migrate 
    """
    config=request.get_json()
    schema_name=config.get('schema_name')
    version=config.get('version', 'latest')
    try:
        importer = Importer(config.get('recipe_engine'), 
                            config.get('build_engine'))
        importer.import_table(schema_name=schema_name, 
                                version=version)
        return jsonify({
            'status': 'success', 
            'schema_name': schema_name,
            'version': version
        })
    except: 
        return jsonify({
            'status': 'failure', 
            'schema_name': schema_name,
            'version': version 
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