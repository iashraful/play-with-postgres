"""
Random user will be fetched from API (https://randomuser.me/)
According to our predefined database tables (users and user_meta) we are going to save the items to table
"""
from dotenv import load_dotenv
import json
from typing import List, Tuple, Any
from uuid import UUID

import requests

from src.database import connect_to_db, close_db_connection


def has_qoute(value: Any):
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value)
    elif isinstance(value, str) and "'" in value:
        return value.replace("'", "")
    return value


def generate_insert_query(data: dict, table_name: str) -> str:
    columns = ",".join([f" {k}" for k in data.keys()])
    values = ",".join([f"'{has_qoute(k)}'" for k in data.values()])
    stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    stmt = stmt.replace("'None'", "'NULL'")
    return stmt


class RandomUser:
    api_base_url = "https://randomuser.me/api/"

    def call_api(self, results: int = 100) -> List[dict]:
        _url = f"{self.api_base_url}?results={results}"
        response = requests.get(_url)
        if response.status_code == 200:
            return response.json()["results"]

    def prepare_user_data(self, data: List[dict]) -> Tuple[List[dict], List[dict]]:
        user_table_data: List[dict] = list()
        user_table_meta_data: List[dict] = list()
        for each in data:
            _user_id = UUID(each["login"]["uuid"])
            user_table_data.append({
                "id": _user_id,
                "first_name": each["name"]["first"],
                "last_name": each["name"]["last"],
                "email": each["email"],
                "phone": each["phone"],
                "photo": each["picture"]["thumbnail"],
                "gender": each["gender"],
            })
            user_table_meta_data.append({
                "user_id": _user_id,
                "title": each["name"]["title"],
                "street": f'{each["location"]["street"]["number"]}{each["location"]["street"]["name"]}',
                "city": each["location"]["city"],
                "state": each["location"]["state"],
                "country": each["location"]["country"],
                "postcode": each["location"]["postcode"],
                "latitude": each["location"]["coordinates"]["latitude"],
                "longitude": each["location"]["coordinates"]["longitude"],
                "timezone": each["location"]["timezone"]["description"],
                "timezone_offset": each["location"]["timezone"]["offset"],
                "dob": each["dob"]["date"],
                "age": each["dob"]["age"],
                "picture": each["picture"]["large"],
                "nationality": each["nat"],
            })

        return user_table_data, user_table_meta_data

    def handler(self):
        results: List[dict] = self.call_api(results=2)
        user_table_data, meta_table_data = self.prepare_user_data(data=results)
        # Connect to database
        connection = connect_to_db()
        try:
            for data in user_table_data:
                sql = generate_insert_query(data=data, table_name="users")
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.commit()
            for data in meta_table_data:
                sql = generate_insert_query(data=data, table_name="user_meta")
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.commit()
        except Exception as err:
            print(err)
        finally:
            close_db_connection(connection=connection)


if __name__ == "__main__":
    load_dotenv(".env")
    api = RandomUser()
    api.handler()
