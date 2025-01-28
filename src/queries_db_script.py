# to handle SQL injection
def sanitize_input(input_string):
    sanitized_string = ''.join(
        char for char in input_string if char.isalnum() or char.isspace() or char == "'" or char == "-")
    return sanitized_string



def query_1(season, year, min_revenue: int):
    query = f"""
                WITH Seasons AS (
                    SELECT 'winter' AS season, 1 AS month
                    UNION ALL
                    SELECT 'winter', 2
                    UNION ALL
                    SELECT 'spring', 3
                    UNION ALL
                    SELECT 'spring', 4
                    UNION ALL
                    SELECT 'spring', 5
                    UNION ALL
                    SELECT 'summer', 6
                    UNION ALL
                    SELECT 'summer', 7
                    UNION ALL
                    SELECT 'summer', 8
                    UNION ALL
                    SELECT 'fall', 9
                    UNION ALL
                    SELECT 'fall', 10
                    UNION ALL
                    SELECT 'fall', 11
                    UNION ALL
                    SELECT 'winter', 12
                )
                SELECT g.genre_name, AVG(m.movie_popularity) AS avg_popularity, SUM(f.revenue) AS total_revenue
                FROM idorosiner.Movies m
                JOIN Seasons s ON MONTH(m.release_date) = s.month
                JOIN idorosiner.MovieGenres g ON m.movie_id = g.movie_id
                JOIN idorosiner.MovieFinances f ON m.movie_id = f.movie_id
                WHERE s.season = '{season}'
                AND YEAR(m.release_date) = {year}
                AND f.revenue >= {min_revenue}
                GROUP BY g.genre_name
                ORDER BY avg_popularity DESC
                LIMIT 5
            """
  
    return query


def query_2(primary_actor: str):
    if not primary_actor:
        print("Input cannot be empty")
        return
    primary_actor = sanitize_input(primary_actor)
    query = f"""
                SELECT a2.actor_name AS secondary_actor, COUNT(*) AS movies_together
                FROM Movies m
                JOIN MovieActors ma1 ON m.movie_id = ma1.movie_id
                JOIN MovieActors ma2 ON m.movie_id = ma2.movie_id
                JOIN Actors a1 ON ma1.actor_id = a1.actor_id
                JOIN Actors a2 ON ma2.actor_id = a2.actor_id
                WHERE a1.actor_name = '{primary_actor}' 
                  AND a2.actor_name != '{primary_actor}'
                GROUP BY a2.actor_name
                ORDER BY movies_together DESC
                LIMIT 2
            """
    return query


def query_3(movie_name: str):
    if not movie_name:
        print("Input cannot be empty")
        return
    movie_name = movie_name.lower()
    query = f"""
                SELECT 
                m.title, 
                m.vote_average, 
                m.overview, 
                m.runtime, 
                GROUP_CONCAT(mp.provider_name) AS Available_On
                FROM 
                idorosiner.Movies m
                LEFT JOIN 
                idorosiner.MovieProviders mp 
                ON 
                m.movie_id = mp.movie_id
                WHERE 
                MATCH(m.title) AGAINST('Inception' IN NATURAL LANGUAGE MODE)
                GROUP BY 
                m.movie_id
                ORDER BY 
                m.vote_average DESC;
                """
    return query


def query_4(ranking: int):
    if not isinstance(ranking, int) and not isinstance(ranking, float):
        print("invalid ranking input")
        return
    if ranking < 0 or ranking > 10:
        print("invalid ranking input - please enter ranking between 0 and 10")
        return
    
    query = f"""
                WITH filtered_movies AS (
                SELECT movie_id
                FROM idorosiner.Movies
                WHERE vote_average >= {ranking}                
                )
                SELECT 
                mp.provider_name, 
                COUNT(DISTINCT fm.movie_id) AS Number_of_Unique_Movies
                FROM filtered_movies fm
                JOIN idorosiner.MovieProviders mp
                ON fm.movie_id = mp.movie_id
                GROUP BY mp.provider_name
                ORDER BY COUNT(DISTINCT fm.movie_id) DESC
                LIMIT 1;
                """
    return query


def query_5(free_text: str, genre: str, date: str, runtime: str):
    if not free_text or not genre or not date or not runtime:
        print("Input cannot be empty")
        return
    query = f"""
                select m.title, m.overview, f.revenue, m.vote_average, g.genre_name, m.release_date, m.runtime
                from idorosiner.Movies m
                join idorosiner.MovieGenres g
                on m.movie_id = g.movie_id
                join idorosiner.MovieFinances f
                on m.movie_id = f.movie_id
                where MATCH(m.overview) AGAINST ('{free_text}' in natural language mode)
                    and g.genre_name = '{genre}' 
                    and m.release_date >= {date}
                    and m.runtime > {runtime} """                
                    
                    
    return query
