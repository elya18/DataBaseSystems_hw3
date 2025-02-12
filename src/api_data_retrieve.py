import requests
import mysql.connector
from mysql.connector import errorcode
from create_db_script import connect_to_database

API_KEY = 'b65f2cb3c102760ac5d48f8ead6babb4'


def populate_Movies(connection, movie_id, title, overview, release_date, runtime, movie_popularity, vote_average):
    try:
        cursor = connection.cursor()
        query = ''' 
                    INSERT INTO Movies
                    (movie_id, title, overview, release_date, runtime, movie_popularity, vote_average) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) 
                '''
        record = (movie_id, title, overview, release_date, runtime, movie_popularity, vote_average)
        cursor.execute(query, record)
        connection.commit()
        
    except mysql.connector.Error as e:
        print("Error in populate_Movie(): " + str(e))
        connection.rollback()
        


def populate_MovieFinances(connection, movie_id, revenue):
    try:
        cursor = connection.cursor()
        query = ''' 
                    INSERT INTO MovieFinances
                    (movie_id, revenue) 
                    VALUES (%s, %s)
                '''
        record = (movie_id, revenue)
        cursor.execute(query, record)
        connection.commit()
    
    except Exception as e:
        print("Error in populate_MovieFinances(): " + str(e))
        connection.rollback()



def populate_Genres(connection, genres):
    cursor = connection.cursor()
    query = ''' 
                INSERT INTO Genres (genre_id, genre_name) 
                VALUES (%s, %s) 
            '''

    for genre in genres:
        record = (genre["id"], genre["name"])
        try:    
            cursor.execute(query, record)
            connection.commit()
        
        except mysql.connector.Error as e:
            # ignore errors involving genre duplication
            if e.errno != errorcode.ER_DUP_ENTRY:
                print("Error in Genres(): " + str(e))
                connection.rollback()
            


def populate_MovieGenres(connection, movie_id, genres):
    try:
        cursor = connection.cursor()
        query = ''' 
                    INSERT INTO MovieGenres (movie_id, genre_id) 
                    VALUES (%s, %s) 
                '''

        for genre in genres:
            record = (movie_id, genre["id"])
            cursor.execute(query, record)

        connection.commit()
    
    except mysql.connector.Error as e:
        print("Error in MovieGenres(): " + str(e))
        connection.rollback()



def populate_Actors_and_MovieActors(connection, movie_id):
    cursor = connection.cursor()
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
    response = requests.get(url)
    cast = response.json()['cast']

    # Iterate over all members of the cast and identify the actors
    for member in cast:
        if member['known_for_department'] == "Acting":
            actor_id = member['id']
            actor_name = member['name']
            actor_gender = 'F' if member['gender'] == 1 else 'M'
            actor_popularity = member['popularity']
            
            try:
                query = ''' 
                            INSERT INTO Actors
                            (actor_id, actor_name, actor_gender, actor_popularity) 
                            VALUES (%s, %s, %s, %s) 
                        '''
                record = (actor_id, actor_name, actor_gender, actor_popularity)
                cursor.execute(query, record)
                connection.commit()
            
            except mysql.connector.Error as e:
                # ignore errors involving actor duplication
                if e.errno != errorcode.ER_DUP_ENTRY:
                    print("Error in populate_Actors(): " + str(e))
                    connection.rollback()
            
            try:
                query = ''' 
                            INSERT INTO MovieActors
                            (movie_id, actor_id) 
                            VALUES (%s, %s) 
                        '''
                record = (movie_id, actor_id)
                cursor.execute(query, record)
                connection.commit()
            
            except Exception as e:
                # ignore errors involving actor duplication
                if e.errno != errorcode.ER_DUP_ENTRY:
                    print("Error in populate_MovieActors(): " + str(e))
                    connection.rollback()



def populate_MovieProviders(connection, movie_id):
    cursor = connection.cursor()
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}'
    response = requests.get(url)
    countries = response.json()['results']
    
    # only insert movies that are availabe in Israel
    if 'IL' in countries:
        query = ''' 
                    INSERT INTO MovieProviders 
                    (movie_id, provider_name) 
                    VALUES (%s, %s) 
                '''
            
        for payment_type in ['rent', 'buy', 'flatrate']:
            if payment_type not in countries['IL']:
                continue
            
            try:
                for provider in countries['IL'][payment_type]:
                    record = (movie_id, provider['provider_name'])
                    cursor.execute(query, record)
                
                connection.commit()
            
            except Exception as e:
                # ignore error involving provider duplication
                if e.errno != errorcode.ER_DUP_ENTRY:
                    print("Error in populate_MovieProviders(): " + str(e))
                    connection.rollback()
                    

def populate_tables():
    max_num_pages = 80
    connection = connect_to_database()

    # Populate all other tables
    for PAGE in range(1, max_num_pages + 1):
        # Get top rated movies
        url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&page={PAGE}'
        response = requests.get(url)
        movies = response.json()['results']
        
        for movie in movies:
            movie_id = movie['id']
            title = movie['title']
            overview = movie['overview']
            release_date = movie['release_date']
            movie_popularity = movie['popularity']
            vote_average = movie['vote_average']
            
            # Get more details on movie
            url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
            response = requests.get(url)
            more_movie_details = response.json()
            
            revenue = more_movie_details['revenue']
            runtime = more_movie_details['runtime']
            genres = more_movie_details['genres']
            
            # populate all the tables
            populate_Movies(connection, movie_id, title, overview, release_date, runtime, movie_popularity, vote_average)
            populate_Genres(connection, genres)
            populate_MovieFinances(connection, movie_id, revenue)
            populate_MovieGenres(connection, movie_id, genres)
            populate_Actors_and_MovieActors(connection, movie_id)
            populate_MovieProviders(connection, movie_id)

    connection.close()
    print("Finished populating all tables")
