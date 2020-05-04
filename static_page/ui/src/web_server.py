from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.response import FileResponse
import mysql.connector as mysql
import json
import requests

USERS_FILE_PATH = "database.txt"
import os
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

#--- the server starts up on the home page
def server_start(req):
  return FileResponse('templates/home_page.html')

#--- this route will show the signup page
def sign_up(req):
  return render_to_response("templates/sign_up.html", {}, request=req)

#--- this route will show the home page
def get_home(req):
  return render_to_response('templates/home_page.html', {}, request=req)

#--- this route will show the about us page
def get_about(req):
  return render_to_response("templates/about_us.html", {}, request=req)

#___ this route will show the pricing page
def get_price(req):
  return render_to_response("templates/Pricing.html", {}, request=req)

#___ this route will show the pricing page
def get_prod_info(req):
  return render_to_response("templates/Product Features.html", {}, request=req)

def sign_up_submit(req):
  fname = req.POST['fname']
  email = req.POST['email']
  lname = req.POST['lname']

  save_user_details(fname, lname, email)

  return Response("Success!!")

def save_user_details(fname, lname, email):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "insert into Users (fname,lname,email) values (%s, %s, %s)"
  values = [
    (fname,lname,email)
  ]
  cursor.executemany(query, values)
  db.commit()
  db.close


if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('start', '/')
  config.add_view(server_start, route_name='start')

  config.add_route('home', '/home')
  config.add_view(get_home, route_name='home')

  config.add_route('sign_up_submit', '/sign_up_submit')
  config.add_view(sign_up_submit, route_name='sign_up_submit', request_method="POST")

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')

  config.add_route('about_us', '/about_us')
  config.add_view(get_about, route_name='about_us')

  config.add_route('pricing', '/pricing')
  config.add_view(get_price, route_name='pricing')

  config.add_route('product_features', '/product_features')
  config.add_view(get_prod_info, route_name='product_features')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
