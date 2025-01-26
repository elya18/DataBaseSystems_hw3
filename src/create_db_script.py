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


def create_Movies(connection):
    # Movies(movie_id(primary key), title(full text index), overview, release_date,runtime,movie_rank(index), is_on_Netflix,is_on_AppleTV,is_on_AmazonPrime)
    cursor = connection.cursor()
    query = """ CREATE TABLE Movies (
                movie_id INT PRIMARY KEY, 
                title varchar(500) NOT NULL, 
                overview varchar(1500),
                release_date DATE NOT NULL,
                runtime smallint NOT NULL,
                movie_popularity FLOAT NOT NULL,
                vote_average FLOAT NOT NULL,
                FULLTEXT(title),
                FULLTEXT(overview),
                INDEX(release_date),
                INDEX(runtime)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating Movies table: " + str(e))
        connection.rollback()


def create_MovieProviders(connection):
    # Movies(movie_id(primary key), provider(full text index))
    cursor = connection.cursor()
    query = """ CREATE TABLE MovieProviders (
                movie_id INT, 
                provider_name varchar(100), 
                FULLTEXT(provider_name),
                PRIMARY KEY (movie_id, provider_name),
                foreign key(movie_id) references Movies(movie_id)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieProviders table: " + str(e))
        connection.rollback()
    

def create_MovieFinances(connection):
    # MoviesFinance(movie_id, budget, revenue)
    cursor = connection.cursor()
    query = """ CREATE TABLE MovieFinances (
                movie_id INT PRIMARY KEY, 
                budget BIGINT NOT NULL,
                revenue BIGINT NOT NULL,
                gross_profit BIGINT NOT NULL,
                foreign key(movie_id) references Movies(movie_id)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieFinances table: " + str(e))
        connection.rollback()

    
def create_MovieGenres(connection):
    # Genres(genre_id, genre_name)
    cursor = connection.cursor()
    query = """ CREATE TABLE MovieGenres (
                movie_id INT, 
                genre_id INT,
                genre_name varchar(50) NOT NULL,
                PRIMARY KEY (movie_id, genre_id),
                foreign key(movie_id) references Movies(movie_id),
                FULLTEXT(genre_name)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieGenres table: " + str(e))
        connection.rollback()


def create_Actors(connection):
    # Actors(actor_id, actor_name(full text index), gender, actor_popularity)
    cursor = connection.cursor()
    query = """ CREATE TABLE Actors (
                actor_id INT PRIMARY KEY, 
                actor_name varchar(100) NOT NULL, 
                actor_gender enum('F','M') NOT NULL, 
                actor_popularity FLOAT NOT NULL,
                FULLTEXT(actor_name)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating Actors table: " + str(e))
        connection.rollback()
    
    
def create_MovieActors(connection):
    # MovieActor(movie_id(primary key), genre_id(primary key))
    cursor = connection.cursor()
    query = """ CREATE TABLE MovieActors (
                movie_id INT, 
                actor_id INT, 
                PRIMARY KEY (movie_id, actor_id),
                foreign key(movie_id) references Movies(movie_id),
                foreign key(actor_id) references Actors(actor_id)
            ) """
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error creating MovieActors table: " + str(e))
        connection.rollback()
    

def create_all_tables():
    connection = connect_to_database()
    create_Movies(connection)
    create_MovieGenres(connection)
    create_MovieFinances(connection)
    create_Actors(connection)
    create_MovieActors(connection)
    create_MovieProviders(connection)
    connection.close()

if __name__ == "__main__":
    create_all_tables()
