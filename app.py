from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Song, Playlist
from forms import SongForm, PlaylistForm, AddSongToPlaylistForm
import os
from dotenv import load_dotenv

# ---- App setup ----
load_dotenv()  # reads .env in your project root

app = Flask(__name__)

# pull connection string from env and force SSL (required by Supabase)
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL not set. Put it in a .env file.")
if "sslmode=" not in db_url:
    db_url += ("&" if "?" in db_url else "?") + "sslmode=require"

app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),  # replace in prod
    SQLALCHEMY_DATABASE_URI=db_url,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

# ---- Home ----
@app.route("/")
def home():
    return redirect(url_for("list_playlists"))

# ---- Songs ----
@app.route("/songs")
def list_songs():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def song_detail(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)

@app.route("/songs/new", methods=["GET", "POST"])
def new_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(song)
        db.session.commit()
        flash("Song added successfully!")
        return redirect(url_for("list_songs"))
    return render_template("new_song.html", form=form)

# ---- Playlists ----
@app.route("/playlists")
def list_playlists():
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def playlist_detail(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)

@app.route("/playlists/new", methods=["GET", "POST"])
def new_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(playlist)
        db.session.commit()
        flash("Playlist created successfully!")
        return redirect(url_for("list_playlists"))
    return render_template("new_playlist.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET","POST"])
def add_song_to_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = AddSongToPlaylistForm()

    # songs NOT already in this playlist
    existing_ids = {s.id for s in playlist.songs}
    choices = [(s.id, f"{s.title} — {s.artist}")
               for s in Song.query.order_by(Song.title)
               if s.id not in existing_ids]

    if not choices:
        flash("No available songs to add. Create one first.")
        return redirect(url_for("new_song"))

    form.song.choices = choices

    if form.validate_on_submit():
        song = Song.query.get_or_404(form.song.data)
        if song.id not in existing_ids:
            playlist.songs.append(song)
            db.session.commit()
            flash(f"Added {song.title} to {playlist.name}!")
        else:
            flash("That song is already in the playlist.")
        return redirect(url_for("playlist_detail", playlist_id=playlist.id))

    return render_template("add_song_to_playlist.html", form=form, playlist=playlist)


# ---- Run directly ----
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
