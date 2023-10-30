
# Task 1: Setting up the Flask application

# Impport all the necessary packages and modules
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import os
import datetime
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
 
# create new flask application 
app = Flask(__name__)

# Connect Flask application with the MySQL 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ganesha@9342'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'library'
app.config['SECRET_KEY'] = '123456' 
mysql = MySQL(app)



# Task 2: Error Handling for all routes and endpoints

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request', 'message' : e}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'error': 'Unauthorized', 'message' : e}), 401

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not Found', 'message' : e}), 404

@app.errorhandler(403)
def already_exists(e):
    return jsonify({'error': 'Already Exists', 'message' : e}), 403

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500


 
# Task 3: Authentication : Implement authentication using JWT Authentication.

# Created a user model with username and password fields.
users = {'pavithra': generate_password_hash('pavi1234')}

# Implemented a login endpoint that authenticates the user and returns a JWT token.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username in users and check_password_hash(users[username], password):
        # Created a JWT token with a short expiration time
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        token = jwt.encode({'username': username, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'access_token': token}), 200
    else:
        return unauthorized('Invalid credentials')

# Implemented a protected endpoint (requires a valid JWT token)
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return unauthorized('Token is missing')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = payload['username']
        return jsonify({'message': 'You have access to this protected resource, {}'.format(current_user)}), 200
    except ExpiredSignatureError:
        return unauthorized('Token has expired')
    except InvalidTokenError:
        return unauthorized('Invalid token')
    except Exception as e:
        return internal_server_error(str(e))



# Task 4: File Handling

# Setting up the necessary file upload configurations and path
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['CONTENT_UPLOAD_TYPE'] = ['jpg', 'jpeg', 'png', 'gif']
app.config['UPLOAD'] = os.path.join(app.root_path, 'static/photos')

# function to verify document type uploaded
def permitted_document(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['CONTENT_UPLOAD_TYPE'] 

# Endpoint that allows users to upload files.
@app.route('/upload', methods=['POST'])
def upload_photo():
    try: 
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(permitted_document(file.filename))
        if file and permitted_document(file.filename):
            file.save(os.path.join(app.config['UPLOAD'], file.filename))
            return jsonify({"message": "Photo uploaded successfully"}), 200
        else:
            return bad_request('Photo could not be uploaded. Make sure to check format!')
    except Exception as e:
        return internal_server_error(str(e))
    


# Task 5: Public Route

# list of items that is returned as part of public route
classes = {
    "software architecture" : "123",
    "machine learning" : "234"
}

# Implemented an endpoint that returns a list of items that can be viewed publicly with no authentication
@app.route('/public_route', methods=['GET'])
def public_route():
    return classes




# Task 6: Services : Implemented web services to perform crud operations in MySQl

# Add a new book into Titan Gallery
@app.route('/add_book', methods=['POST'])
def add_book():
            book = request.args.get('book')
            author = request.args.get('author')
            publication = request.args.get('publication')
            print(book,author,publication)
            # Check if the book already exists
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM gallery WHERE book=%s", [book])
            exisiting_book = cur.fetchone()
            cur.close()
            if exisiting_book:
                return already_exists({"message": "Book already exists"})
            else:
                # create new book
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO gallery(book, author, publication) VALUES (%s, %s, %s)", [book, author, publication])
                mysql.connection.commit()
                cur.close()
                return jsonify("Book added/created!"), 200 

# Update an exisiting book in Titan Gallery
@app.route('/update_book', methods=['PUT'])
def update_book():
            book = request.args.get('book')
            author = request.args.get('author')
            publication = request.args.get('publication')

            # Check if the username is already in use
            cur = mysql.connection.cursor() 
            cur.execute("SELECT * FROM gallery WHERE book= %s", [book])
            exisiting_book = cur.fetchone()
            cur.close()
            if exisiting_book:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE gallery SET author=%s,publication=%s WHERE book=%s",[author, publication, book])
                mysql.connection.commit()
                cur.close()
                return jsonify("Book details updated!"), 200 
            else:
                return not_found("Book does not exist")
            
# Update an exisiting book in Titan Gallery           
@app.route('/delete_book', methods=['DELETE'])
def delete_book():
            book = request.args.get('book')
            # Check if the book is exisiting
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM gallery WHERE book= %s", [book])
            exisiting_book = cur.fetchone()
            cur.close()
            if exisiting_book:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM gallery WHERE book= %s", [book])
                mysql.connection.commit()
                cur.close()
                return jsonify("Book deleted!"), 200 
            else:
                return not_found("Book does not exist to be deleted!")

# Get all books exisiting in Titan Gallery              
@app.route('/all_book', methods=['GET'])
def all_books():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM gallery")
            books = cur.fetchall()
            cur.close()
            return jsonify(books), 200 



# home page for the app
@app.route('/')
def home():
    return "Welcome Titan!"

if __name__ == '__main__':
    app.run(debug=True)
