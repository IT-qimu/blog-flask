#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/2 13:41
author:    peak
description:
"""
from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g
import datetime, os
from app.models import db, User, Comment, Post, Tag, tags
from app.markdown_html import switch_html
from werkzeug.utils import secure_filename

post = Blueprint(
    'post',
    __name__
)

@post.route('/post/<int:year>/<int:month>/<int:id>', methods=['GET', 'POST'])
def postdetails(year,month,id):
    lenth = 0
    comments = Comment.query.filter(Comment.Post_Id == id).order_by(Comment.Id.desc()).all()
    lenth = len(comments)
    global lenth
    global comments

    content = ""
    posts = Post.query.filter(Post.User_Id == 1, Post.Id == id).first()
    post_file = posts.Content_Name
    basepath = os.path.abspath(os.path.dirname(__file__))       # 当前文件所在目录
    parentdir = os.path.dirname(basepath)                       # 父级目录
    if post_file != None:
        post_file_url = os.path.join(parentdir, 'static/Upload_Files/markdown', secure_filename(post_file))
        content = switch_html(post_file_url)



    if request.method == "POST":
        commentforsql = Comment()
        commentforsql.Name = request.form.get("nickname")
        commentforsql.Email = request.form.get("email")
        commentforsql.text = request.form.get("leavemessage")
        commentforsql.Post_Id = id

        db.session.add(commentforsql)
        db.session.commit()

        comments = Comment.query.filter(Comment.Post_Id == id).order_by(Comment.Id.desc()).all()
        lenth = len(comments)
        return render_template('Post_Details.html', posts=posts, content=content, lenth=lenth, comments=comments, title=posts.Title)

    return render_template('Post_Details.html', posts=posts, content=content, lenth=lenth, comments=comments, title=posts.Title)

@post.route('/tag/<int:tagid>', methods=['GET', 'POST'])
def tag(tagid):
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        TAG = Tag.query.filter(Tag.Id == tagid).first()
        POST = TAG.posts
        pagination = POST.order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        tem = []
        for x in user_Post:
            tem.append(x.to_json())
        print jsonify(tem)
        return jsonify(objects = tem)

    if request.method == 'GET':
        page = request.form.get('page', 1)
        page = int(page)
        TAG = Tag.query.filter(Tag.Id == tagid).first()
        POST = TAG.posts
        pagination = POST.order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        return render_template('tag_details.html', user_Post=user_Post, lenth=lenth, pagination=pagination, title=TAG.Title)