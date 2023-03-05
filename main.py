import os
import datetime
import pytz
import requests
from pprint import pprint
from notion_client import Client

def get_notion_client():
    token = os.environ.get("NOTION_TOKEN")
    notion = Client(auth=token)
    return notion

def list_notion_users():
    notion = get_notion_client()
    list_users_response = notion.users.list()
    pprint(list_users_response)

def get_notion_database():
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {os.environ.get('NOTION_TOKEN')}"
    }
    json_data = {
        "sort": {
            "direction": "ascending",
            "timestamp": "last_edited_time"
        }
    }
    url = "https://api.notion.com/v1/search"
    response = requests.post(url, json=json_data, headers=headers)
    data = response.json()
    return data.get("results")[0].get("id")

def create_notion_page():
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {os.environ.get('NOTION_TOKEN')}"
    }
    database_id = get_notion_database()
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    date = format(today, '%Y-%m-%d')
    json_data = {
        "parent": {
            "database_id": database_id
        },
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "タイトルタイトル"
                        }
                    }
                ]
            },
            "期限": {
                "date": {
                    "start": date
                }
            },
            "メモ": {
                "rich_text": [
                    {
                        "text": {
                            "content": "メモメモ"
                        }
                    }
                ]
            }
        }
    }
    url = "https://api.notion.com/v1/pages"
    response = requests.post(url, json=json_data, headers=headers)
    print(response.text)

if __name__ == "__main__":
    list_notion_users()
    create_notion_page()
