import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient
from io import BytesIO
from PIL import Image

# Azure Blob Storageの接続情報
connect_str = 'DefaultEndpointsProtocol=https;AccountName=aigallery;AccountKey=qyljkC1sn1IrirPS0PsgiocbNitV2Ar7RhA2R4y4Z8SiCOIdlHh5mh5+maR7x8yq8KiaLlvQUwU2+ASt/d2Lfg==;EndpointSuffix=core.windows.net'
container_name = 'aigallery'

# BlobServiceClientのインスタンス化
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# コンテナの参照
container_client = blob_service_client.get_container_client(container_name)

# コンテナ内の全てのBlob名をリストで取得
blob_list = [b.name for b in container_client.list_blobs()]

# 各BlobのURLをリストに格納
url_list = [container_client.get_blob_client(blob).url for blob in blob_list]

# 各画像を縦一列に表示
for url in url_list:
    # URLからBlobClientのインスタンスを生成
    blob_client = BlobClient.from_blob_url(url)
    # Blobから画像ファイルのバイナリデータを取得
    img_binary = blob_client.download_blob().readall()
    # バイナリデータからPIL.Imageを生成
    img = Image.open(BytesIO(img_binary))
    # 画像を表示
    st.image(img, use_column_width=True)
