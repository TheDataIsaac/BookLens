import psycopg2



class Database:
    def __init__(self):
        # Establish a connection to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname='booklens',
            user='classicisaac',
            password='thimmy',
            host='localhost',
            port='5432'
        )
        self.cur = self.conn.cursor()

        # Create the books table if not exists
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR,
                author VARCHAR,
                price FLOAT,
                description TEXT,
                rating FLOAT,
                num_of_rating INT,
                publisher VARCHAR,
                language VARCHAR,
                paperback VARCHAR,
                item_weight VARCHAR,
                dimensions VARCHAR         
            )
        ''')

        self.conn.commit()

        # Create the reviews table if not exists
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                reviewer_name VARCHAR(100),
                review_rating FLOAT,
                review_title VARCHAR(500),
                review_date DATE,
                review_content TEXT,
                book_id INT,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        self.conn.commit()
