from flask import Flask, render_template, request, redirect, url_for
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'dj'
app.config[
    'BASIC_AUTH_PASSWORD'] = 'password'  # Change this to a secure password
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///song_requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basic_auth = BasicAuth(app)
db = SQLAlchemy(app)


class SongRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song = db.Column(db.String(100), nullable=False)
    requester = db.Column(db.String(100), nullable=False)
    played = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    song_requests = SongRequest.query.all()
    return render_template('index.html', song_requests=song_requests)


@app.route('/request', methods=['POST'])
def song_request():
    song_name = request.form.get('song_name')
    requester_name = request.form.get('requester_name')
    if song_name and requester_name:
        new_request = SongRequest(song=song_name, requester=requester_name)
        db.session.add(new_request)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/dj')
@basic_auth.required
def dj_page():
    song_requests = SongRequest.query.all()
    return render_template('dj.html', song_requests=song_requests)


@app.route('/dj/delete', methods=['POST'])
@basic_auth.required
def dj_delete_song():
    song_name = request.form.get('song_name')
    song_request = SongRequest.query.filter_by(song=song_name).first()
    if song_request:
        db.session.delete(song_request)
        db.session.commit()
    return redirect(url_for('dj_page'))


@app.route('/dj/played', methods=['POST'])
@basic_auth.required
def dj_played_song():
    song_name = request.form.get('song_name')
    song_request = SongRequest.query.filter_by(song=song_name).first()
    if song_request:
        song_request.played = not song_request.played
        db.session.commit()
    return redirect(url_for('dj_page'))


@app.route('/tip')
def tip():
    return redirect("https://venmo.com/u/bhandari725", code=302)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
