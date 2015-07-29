# pri-gpio
Raspberry PI GPIO web project

<b>1. Install uptime.</b></br>
<code>pip install uptime</code></br>
<b>2. Set up database and create user with 0 privileges.</b></br>
&emsp;2.1 Make migrations in the application:</br>
 &emsp; <code>python manage.py makemigrations</code></br>
&emsp;2.2 Sync models with database:</br>
 &emsp; <code>python manage.py syncdb</code></br>
&emsp;2.3 Run python shell and add superuser:</br>
 &emsp; <code>python manage.py shell</code></br>
 &emsp; <code>>>>from models import *</code></br>
 &emsp; <code>>>>u=User.objects.create_user(username=u'somename')</code></br>
 &emsp; <code>>>>u.set_password(u'some_pass')</code></br>
 &emsp; <code>>>>u.save()</code></br>
 &emsp; <code>>>>cu=ControllUser(user=u, privig=0)</code></br>
&emsp; <code>>>>cu.save()</code></br>
<b>3. Run django server on port 8000 with sudo</b></br>
 &emsp; <code>sudo python manage.py runserver 8000</code></br>
<b>4. Сopy file <code>configs/raspi-gpio.conf</code> to <code>/etc/nginx/sited-enabled</code> and restart nginx</b></br>
 &emsp; <code>sudo service nginx restart</code></br>
