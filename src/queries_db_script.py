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
                SELECT g.genre_name, AVG(r.movie_popularity) AS avg_popularity, SUM(f.revenue) AS total_revenue
                FROM Movies m
                JOIN Seasons s ON MONTH(m.release_date) = s.month
                JOIN Reviews r ON r.movie_id = m.movie_id
                JOIN Genres g ON m.movie_id = g.movie_id
                JOIN Movies_Finance f ON m.movie_id = f.movie_id
                WHERE s.season = '{season}'
                  AND YEAR(m.release_date) = '{year}'
                  AND f.revenue >= {min_revenue}
                GROUP BY g.genre_name
                ORDER BY avg_popularity DESC
                LIMIT 10
            """
    return query


def query_3(movie_name: str):
    if not movie_name:
        print("Input cannot be empty")
        return
    movie_name = movie_name.lower()
    query = f"""
                SELECT Movies.title, Movies.rank, Movies.overview, Movies.runtime, Movies.is_on_Netflix as Netflix, 
                Movies.is_on_AppleTV as AppleTV, Movies.is_on_AmazonPrime as AmazonPrime
                From Movies
                WHERE MATCH(Movies.title) AGAINST('{movie_name}' in natural language mode)
                ORDER BY Movies.rank DESC"""
    return query


def query_4(ranking: int):
    if not isinstance(ranking, int) and not isinstance(ranking, float):
        print("invalid ranking input")
        return
    if(ranking < 0 or ranking > 10):
        print("invalid ranking input - please enter ranking between 0 and 10")
        return
    query = """
                WITH filtered_movies AS (
                SELECT movie_id, is_on_Netflix,is_on_AppleTV,is_on_AmazonPrime
                FROM Movies
                WHERE rank >= %s
                ),
                Netflix AS (
                SELECT COUNT(movie_id) AS Number_of_Unique_Movies
                FROM filtered_movies
                WHERE is_on_Netflix = 1 AND is_on_AppleTV = 0 AND is_on_AmazonPrime = 0
                ),
                AppleTV AS (
                SELECT COUNT(movie_id) AS Number_of_Unique_Movies
                FROM filtered_movies
                WHERE is_on_AppleTV = 1 AND is_on_Netflix = 0 AND is_on_AmazonPrime = 0
                ),
                AmazonPrime AS (
                SELECT COUNT(movie_id) AS Number_of_Unique_Movies
                FROM filtered_movies
                WHERE is_on_AmazonPrime = 1 AND is_on_Netflix = 0 AND is_on_AppleTV = 0
                )
                SELECT Streaming_Service, Number_of_Unique_Movies
                FROM (
                SELECT 'Netflix' AS Streaming_Service, Number_of_Unique_Movies FROM Netflix
                UNION ALL
                SELECT 'AppleTV' AS Streaming_Service, Number_of_Unique_Movies FROM AppleTV
                UNION ALL
                SELECT 'AmazonPrime' AS Streaming_Service, Number_of_Unique_Movies FROM AmazonPrime
                ) AS streaming_counts
                WHERE Number_of_Unique_Movies >= ALL (
                SELECT MAX(max_count)
                FROM (
                SELECT MAX(Number_of_Unique_Movies) AS max_count FROM Netflix
                UNION ALL
                SELECT MAX(Number_of_Unique_Movies) AS max_count FROM AppleTV
                UNION ALL
                SELECT MAX(Number_of_Unique_Movies) AS max_count FROM AmazonPrime
                ) AS max_counts
                );
            """
    return query


def query_5(free_text: str, genre: str, date: str, runtime: str):
    if not free_text or not genre or not date or not runtime:
        print("Input cannot be empty")
        return
    query = f"""select Movies.title, Movies.overview, MoviesFinance.revenue, Reviews.vote_average
                from Movies m
                join Genres g
                on m.movie_id = g.movie_id
                join MoviesFinance f
                on m.movie_id = f.movie_id
                join Reviews re
                on m.movie_id = re.movie_id
                where MATCH(m.overview) AGAINST ('{free_text}' in natural language mode)
                    and MATCH(g.genre_name) AGAINST ('{genre}' in natural language mode)
                    and m.release_date >= '{date}'
                    and m.runtime > {runtime}"""
    return query
