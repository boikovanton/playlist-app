from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many (playlists <-> songs)
playlist_songs = db.Table(
    "playlist_songs",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("songs.id"), primary_key=True),
)


class Song(db.Model):
    """Song model"""
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)

    # relationship: song.playlists -> list of Playlist objects
    playlists = db.relationship("Playlist",
                                secondary=playlist_songs,
                                back_populates="songs")

    def __repr__(self):
        return f"<Song {self.id} {self.title} by {self.artist}>"


class Playlist(db.Model):
    """Playlist model"""
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    # relationship: playlist.songs -> list of Song objects
    songs = db.relationship("Song",
                            secondary=playlist_songs,
                            back_populates="playlists")

    def __repr__(self):
        return f"<Playlist {self.id} {self.name}>"
