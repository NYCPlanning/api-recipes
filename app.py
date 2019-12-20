import os
from flask import Flask, request, jsonify
from s3_utils import make_client, bucket
import pandas as pd

app = Flask(__name__)
client = make_client()

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
    key=request.args['key']
    print(key)
    if request.method == 'DELETE':
        response = client.delete_object(
            Bucket=bucket, 
            Key=key)
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)