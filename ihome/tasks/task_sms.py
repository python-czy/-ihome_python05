from celery import Celery
from ihome.libs.yuntongxun.sms import CCP

# 定义Celery对象
app = Celery("ihome", broker="redis://127.0.0.1:6379/15")


@app.task
def send_sms(to, datas, temp_id):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
