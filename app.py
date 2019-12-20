import os
from flask import Flask, request, jsonify
from utils.s3 import make_client, bucket
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
    key = request.form.get('key', file.filename)
    acl = request.form.get('acl', 'private')
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
    key=request.args['key']
    print(key)
    if request.method == 'DELETE':
        response = client.delete_object(
            Bucket=bucket, 
            Key=key)
        return jsonify(response)

@app.route('/archive', methods=['POST'])
def archive():
    """
    cli version: cook run <recipe>
    by default, cook to recipe database
    whenever a table is updated, also 
    update recipes table, either as a csv
    or in the database
    """

@app.route('/migrate', methods=['POST'])
def migrate():
    """
    migrate table from database A to B
    table_name.version in A 
    to table_name.version in B
    """

@app.route('/download', methods=['GET'])
def download():
    """
    download file from given database to 
    different format using gdal, 
    including csv, shapfiles, geojson
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)