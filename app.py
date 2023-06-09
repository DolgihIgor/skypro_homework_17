# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Str()
    rating = fields.Str()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# Создаем API для нашего Flask приложения
api = Api(app)

# Создадим namespace эндпоинты
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


# ---------------------------------- Movies --------------------------------------- #

@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        # Получаем director_id или genre_id из запроса вида /movies/?director_id=1
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id is not None:
            res = Movie.query.filter(Movie.director_id == director_id)
        if genre_id is not None:
            res = Movie.query.filter(Movie.genre_id == genre_id)
        all_movies = res.all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201, {"Location": f"/movies/{new_movie.id}"}


@movie_ns.route("/<int:uid>")
class MovieView(Resource):
    def get(self, uid: int):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 404
        return movie_schema.dump(movie), 200

    def put(self, uid: int):
        movie = Movie.query.get(uid)
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.genre = req_json.get("genre")
        movie.director_id = req_json.get("director_id")
        movie.director = req_json.get("director")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def patch(self, uid: int):
        movie = Movie.query.get(uid)
        req_json = request.json
        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "genre" in req_json:
            movie.genre = req_json.get("genre")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")
        if "director" in req_json:
            movie.director = req_json.get("director")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 204
        db.session.delete(movie)
        db.session.commit()

# ---------------------------------------- Directors -------------------------------------#
@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201, {"Location": f"/directors/{new_director.id}"}


@director_ns.route("/<int:uid>")
class DirectorView(Resource):
    def get(self, uid: int):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        return director_schema.dump(director), 200

    def put(self, uid: int):
        director = Director.query.get(uid)
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def patch(self, uid: int):
        director = Director.query.get(uid)
        req_json = request.json
        if "name" in req_json:
            director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        if not director:
            return "", 204
        db.session.delete(director)
        db.session.commit()


#----------------------------------- Genres ------------------------------#
@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201, {"Location": f"/genres/{new_genre.id}"}


@genre_ns.route("/<int:uid>")
class GenreView(Resource):
    def get(self, uid: int):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        return genre_schema.dump(genre), 200

    def put(self, uid: int):
        genre = Genre.query.get(uid)
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def patch(self, uid: int):
        genre = Genre.query.get(uid)
        req_json = request.json
        if "name" in req_json:
            genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 204
        db.session.delete(genre)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
