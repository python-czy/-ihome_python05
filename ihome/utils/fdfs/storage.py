from fdfs_client.client import Fdfs_client, get_tracker_conf
from ihome import constants


class FDFSStorage():
    """fast dfs文件存储类"""
    def __init__(self, client_conf=None):
        """初始化"""
        if client_conf is None:
            client_conf = constants.FDFS_CLIENT_CONF_PATH
        self.client_conf = client_conf

    def upload(self, file_data):

        trackers = get_tracker_conf(self.client_conf)
        client = Fdfs_client(trackers)
        res = client.upload_by_buffer(file_data)

        if res.get('Status') != 'Upload successed.':
            return Exception("上传失败")
        else:
            filename = res.get('Remote file_id')
            return filename.decode()

