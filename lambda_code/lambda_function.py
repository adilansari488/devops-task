import json
import os
import psycopg2


def lambda_handler(event, context):
    for record in event['Records']:
        print("record received and processing...")
        message = json.loads(record['body'])
        message_str = json.dumps(message)
        
        try:
            connection = psycopg2.connect(
                host=os.getenv('DB_ENDPOINT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_Name'),
                port=5432
            )
            if connection:
                print("successfully connected to database")
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO messages (message_id, message_content)
                VALUES (%s, %s)
            """
            cursor.execute(insert_query, (record['messageId'], message_str))
            connection.commit()
            print("data inserted into database")
            
        except Exception as e:
            print(f"error connecting to the database or inserting data: {e}")
        
        finally:
            cursor.close()
            connection.close()
            print("database connection closed")

    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }

