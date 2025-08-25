from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class SongForm(FlaskForm):
    """Form to add a new song"""
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    artist = StringField("Artist", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Add Song")


class PlaylistForm(FlaskForm):
    """Form to create a new playlist"""
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Description")
    submit = SubmitField("Create Playlist")


class AddSongToPlaylistForm(FlaskForm):
    """Form to add a song to an existing playlist"""
    song = SelectField("Song", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add to Playlist")
