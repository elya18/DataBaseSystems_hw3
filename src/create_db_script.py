import mysql.connector


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="idorosiner",
            password="idoros22896",
            port=3305,
            database="idorosiner"
        )
        if connection.is_connected():
            print("connected")
            return connection
    except:
        print("Connection failed")
        exit(-1)


# Movies(movie_id, title, overview, release_date, runtime, vote_average)
# Fulltext - title, overview
# Index - release_date, runtime, vote_average
# Primary key - movie_id
def create_Movies(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE Movies (
                    movie_id INT PRIMARY KEY, 
                    title varchar(500) NOT NULL, 
                    overview varchar(1500),
                    release_date DATE NOT NULL,
                    runtime smallint NOT NULL,
                    movie_popularity FLOAT NOT NULL,
                    vote_average FLOAT NOT NULL,
                    FULLTEXT(title),
                    FULLTEXT(overview),
                    INDEX(vote_average),
                    INDEX(release_date),
                    INDEX(runtime)
                )
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating Movies table: " + str(e))
        connection.rollback()


# MovieProviders(movie_id, provider_name)
# Fulltext - provider_name
# Primary key - (movie_id, provider_name)
# Foreign key - movie_id references Movies.movie_id
def create_MovieProviders(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE MovieProviders (
                    movie_id INT, 
                    provider_name VARCHAR(100), 
                    FULLTEXT(provider_name),
                    PRIMARY KEY(movie_id, provider_name),
                    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieProviders table: " + str(e))
        connection.rollback()
    

# MoviesFinance(movie_id, revenue)
# Primary key - movie_id
# Foreign key - movie_id references Movies.movie_id
def create_MovieFinances(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE MovieFinances (
                    movie_id INT PRIMARY KEY, 
                    revenue BIGINT NOT NULL,
                    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieFinances table: " + str(e))
        connection.rollback()

# Genres(genre_id, genre_name)
# Fulltext - genre_name
# Primary key - genre_id
def create_Genres(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE Genres (
                    genre_id INT PRIMARY KEY, 
                    genre_name VARCHAR(50) NOT NULL,
                    FULLTEXT(genre_name)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieActors table: " + str(e))
        connection.rollback()
        
        
# MovieGenres(movie_id, genre_id)
# Primary key - (movie_id, genre_id)
# Foreign key - movie_id references Movies.movie_id
#               genre_id references Genres.genre_id
def create_MovieGenres(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE MovieGenres (
                    movie_id INT, 
                    genre_id INT,
                    PRIMARY KEY(movie_id, genre_id),
                    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id),
                    FOREIGN KEY(genre_id) REFERENCES Genres(genre_id)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieGenres table: " + str(e))
        connection.rollback()


# Actors(actor_id, actor_name, gender, actor_popularity)
# Fulltext - actor_name
# Primary key - actor_id
def create_Actors(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE Actors (
                    actor_id INT PRIMARY KEY, 
                    actor_name VARCHAR(100) NOT NULL, 
                    actor_gender ENUM('F','M') NOT NULL, 
                    actor_popularity FLOAT NOT NULL,
                    FULLTEXT(actor_name)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating Actors table: " + str(e))
        connection.rollback()
    

# MovieActor(movie_id, actor_id)
# Primary key - (movie_id, actor_id)
# Foreign key - movie_id references Movies.movie_id,
#               actor_id references Actors.actor_id
def create_MovieActors(connection):
    cursor = connection.cursor()
    query = """ 
                CREATE TABLE MovieActors (
                    movie_id INT, 
                    actor_id INT, 
                    PRIMARY KEY(movie_id, actor_id),
                    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id),
                    FOREIGN KEY(actor_id) REFERENCES Actors(actor_id)
                ) 
            """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieActors table: " + str(e))
        connection.rollback()
    

def create_all_tables():
    connection = connect_to_database()
    create_Movies(connection)
    create_Genres(connection)
    create_MovieGenres(connection)
    create_MovieFinances(connection)
    create_Actors(connection)
    create_MovieActors(connection)
    create_MovieProviders(connection)
    connection.close()
    print("Finished building all tables")
