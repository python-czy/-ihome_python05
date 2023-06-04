from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request, session
from ihome.utils.response_code import RET
from ihome.utils.fdfs.storage import FDFSStorage
from ihome.models import User
from ihome import db, constants


@api.route("/user/profile", methods=["GET"])
@login_required
def get_user_profile():
    """获取用户个人信息
    数据：用户头像： 用户名 号码
    """
    user_id = g.user_id
    # 查询数据库获取个人信息
    try:
        # user = User.query.filter_by(id=user_id).first()
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="成功", data=user.to_dict())


@api.route("/user/avatar", methods=["POST"])
@login_required
def set_user_avatar():
    """设置用户的头像
    参数：图片（多媒体表单格式）  用户id(g.user_id)
    """
    # 装饰器的代码中已经将user_id 保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    # 获取图片
    image_file = request.files.get("avatar")
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")

    image_data = image_file.read()

    # 调用fdfs上传图片, 返回文件名
    fdfs = FDFSStorage()
    try:
        file_name = fdfs.upload(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    avatar_url = constants.FDFS_SERVER_URL + file_name
    # 保存成功 返回

    return jsonify(errno=RET.OK, errmsg="保存成功", data={"avatar_url": avatar_url})


@api.route("/user/name", methods=["PUT"])
@login_required
def change_user_name():
    """修改用户名
    参数：用户名  用户id(g.user_id)
    """
    # 装饰器的代码中已经将user_id 保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    # 获取用户想要设置的用户名
    # user_name = request.form.get("user_name")
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    user_name = req_data.get("name")  # 用户想要设置的名字
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg="名字不能为空")

    # 校验用户名长度不能超过8位
    if len(user_name) > 8:
        return jsonify(errno=RET.PARAMERR, errmsg="用户名过长")

    # # 校验用户名是否重复
    # try:
    #     user = User.query.filter_by(name=user_name).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")
    #
    # if user is not None:
    #     return jsonify(errno=RET.DATAEXIST, errmsg="用户名已存在")

    # 保存用户名到数据库中，并同时判断name是否重复（利用数据库的唯一索引）
    try:
        User.query.filter_by(id=user_id).update({"name": user_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    # 修改session数据中的name字段
    session["name"] = user_name

    return jsonify(errno=RET.OK, errmsg="OK", data={"name": user_name})


@api.route("/user/auth", methods=["GET"])
@login_required
def get_user_auth():
    """获取用户的实名认证信息"""
    user_id = g.user_id

    # 在数据库中查询信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


@api.route("/user/auth", methods=["POST"])
@login_required
def set_user_auth():
    """用户实名认证
    参数：用户id  真实姓名 身份证号码
    格式：表单
    """
    user_id = g.user_id
    # 获取参数
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    real_name = req_data.get("real_name")  # 真实姓名
    id_card = req_data.get("id_card")   # 身份证号

    # 校验参数
    # 校验参数的完整性
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 校验数据的正确性
    # 身份证号为18位
    if len(id_card) != 18:
        return jsonify(errno=RET.PARAMERR, errmsg="数据格式不正确")

    # 业务处理，将信息保存到数据库中
    try:
        # User.query.filter_by(id=user_id, real_name=None, id_card=None)\
        # .update({"real_name": real_name, "id_card": id_card})
        user = User.query.filter_by(id=user_id).first()
        user.real_name = real_name
        user.id_card = id_card
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")

    return jsonify(errno=RET.OK, errmsg="认证成功")











