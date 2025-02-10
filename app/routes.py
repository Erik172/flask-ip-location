from datetime import datetime
from flask import request, render_template, redirect, url_for, current_app as app
from app import db
from app.models import IPLocation, URL
import requests
import string
import random

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(4))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-url', methods=['POST'])
def create_url():
    original_url = request.form['original_url']
    short_url = generate_short_url()
    
    new_url = URL(original_url=original_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()
    
    return f'URL acortada: {request.host_url}{short_url}'

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    url.visits += 1
    url.last_visited = datetime.now()
    db.session.commit()
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0]  # En caso de múltiples IPs, toma la primera
        
    if ip == '127.0.0.1':
        ip = requests.get('http://ifconfig.me/ip').text
    
    response = requests.get(f'http://ip-api.com/json/{ip}')
    data = response.json()
    print(data)
    
    ip_location = IPLocation(ip=ip, city=data['city'], region=data['region'], country=data['country'], loc=f"{data['lat']}, {data['lon']}")
    
    db.session.add(ip_location)
    db.session.commit()
    
    return redirect(url.original_url)

@app.route('/stats')
def stats():
    urls = URL.query.all()
    return render_template('stats.html', urls=urls)

@app.route('/say-hello/<name>')
def say_hello(name):
    return render_template('hello.html', name=name)