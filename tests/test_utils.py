from discord_to_sqlite.utils import save_channels
from discord_to_sqlite.utils import save_messages
from discord_to_sqlite.utils import save_servers
from discord_to_sqlite.utils import save_users

import sqlite_utils
from .utils import create_zip

def test_users():
    zf = create_zip()
    db = sqlite_utils.Database(memory=True)
    save_users(db, zf)   
    assert "users" in db.table_names()
    users = list(sorted(db["users"].rows, key=lambda r: r["id"]))
    assert [
        {
            "id": 123456789012345678,
            "username": "myself",
            "type": None,
            "nickname": None,
            "avatar": None,
            "discriminator": "1000", 
            "public_flags": None,           
        },
        {
            "id": 234567890123456789,
            "username": "myfriend",
            "type": 1,
            "nickname": None,
            "avatar": "0108d80108d80108d80108d80108d8",
            "discriminator": "0001", 
            "public_flags": 1,           
        },
    ] == users

def test_servers():
    zf = create_zip()
    db = sqlite_utils.Database(memory=True)
    save_servers(db, zf)
    assert "servers" in db.table_names()
    servers = list(db["servers"].rows)
    assert [
        {
            "id": 580762123498765432,
            "name": "LeetGaming"
        },    
    ] == servers

def test_messages():
    zf = create_zip()
    db = sqlite_utils.Database(memory=True)
    # must run servers and channels to create tables for foreign keys
    save_servers(db, zf)
    save_channels(db, zf)
    save_messages(db, zf)  
    assert "messages" in db.table_names()
    messages = list(sorted(db["messages"].rows, key=lambda r: r["id"]))
    assert [
        {
            "id": 591928374747283947,
            "timestamp": "2020-06-20 16:14:02.698000+00:00",
            "contents": "hey mate",
            "attachments": "",
            "channel_id": 239987654456687789,       
        },
        {
            "id": 689524354426288283,
            "timestamp": "2020-10-11 16:48:31.211000+00:00",
            "contents": "sup?",
            "attachments": "",
            "channel_id": 589871236751234678,             
        },
    ] == messages

def test_channels():
    zf = create_zip()
    db = sqlite_utils.Database(memory=True)
    # must run servers to create tables for foreign keys
    save_servers(db, zf)
    save_channels(db, zf)
    assert "channels" in db.table_names()
    my_channels = list(sorted(db["channels"].rows, key=lambda r: r["id"]))
    assert [
        {
            "id": 239987654456687789,
            "type": 1,
            "name": "Direct Message with myfriend#0001",
            "recipients": '["123456789012345678", "234567890123456789"]',
            "guild_id": None,            
        },
        {
            "id": 589871236751234678,
            "type": 0,
            "name": "general",
            "recipients": None,
            "guild_id": 580762123498765432,              
        }
    ] == my_channels
