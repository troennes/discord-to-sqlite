import json
import csv
import os
from io import TextIOWrapper

def save_all(db, zf):
    save_users(db, zf)
    save_servers(db, zf)
    # Has foreign key in servers, must run after save_servers
    save_channels(db, zf) 
    # Has foreign key in channels, must run after save_channels
    save_messages(db, zf)

def save_messages(db, zf):
    messages = [
        f.filename for f in zf.filelist if f.filename.endswith("messages.csv")
    ]
    for filename in messages:
        # extract channel_id from file path (messages/<id>/messages.csv)
        channel_id = int(filename.split(os.sep)[1])
        
        with zf.open(filename) as csvfile:
            # must convert bytes to text with TextIOWrapper for csv.reader
            reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'))
            for row in reader:
                db["messages"].upsert({
                    "id": int(row["ID"]),
                    "timestamp": row["Timestamp"],
                    "contents": str(row["Contents"]),
                    "attachments": str(row["Attachments"]),
                    "channel_id": channel_id
                }, foreign_keys=[
                    ("channel_id", "channels", "id")
                ], pk="id")

def save_servers(db, zf):
    servers = json.load(
        zf.open("servers/index.json")
    )
    for key in servers:
        db["servers"].upsert({
            "id": int(key),
            "name": servers[key],
        }, pk="id", column_order=("id", "name"))

def save_users(db, zf):
    user = json.load(
        zf.open("account/user.json")
    )
    # add friends
    for friend in user["relationships"]:
        nested_user_object = friend["user"]
        db["users"].upsert({
            "id": int(friend["id"]),
            "type": int(friend["type"]),
            "nickname": friend["nickname"],
            "username": nested_user_object["username"],
            "avatar": nested_user_object["avatar"],
            "discriminator": str(nested_user_object["discriminator"]),
            "public_flags": int(nested_user_object["public_flags"]),
        }, pk="id", column_order=(
            "id","username","type","nickname","avatar","discriminator","public_flags"
        ))

    # add self
    db["users"].upsert({
        "id": int(user["id"]),
        "type": None,
        "nickname": None,
        "username": user["username"],
        "avatar": user["avatar_hash"],
        "discriminator": str(user["discriminator"]),
        "public_flags": None,
    }, pk="id", column_order=(
        "id","username","type","nickname","avatar","discriminator","public_flags"
    ))

def save_channels(db, zf):

    channel_names = json.load(
        zf.open("messages/index.json")
    )
    channel_details = [
        f.filename for f in zf.filelist if f.filename.endswith("channel.json")
    ]

    # Ensure correct types in table
    if not "channels" in db.table_names():
        db["channels"].create({
            "id": int,
            "type": int,
            "name": str,
            "recipients": str,
            "guild_id": int,            
        }, 
            foreign_keys=[("guild_id", "servers", "id")],
            pk="id", 
            column_order=("id", "type", "name", "recipients", "guild_id")
        )

    for filename in channel_details:
        contents = json.load(zf.open(filename))
        channel_type = int(contents["type"])
        channel_id = contents["id"]

        if "guild" in contents:
            guild = contents["guild"]
            guild_id = int(guild["id"])
        else:
            guild_id = None
        
        if "recipients" in contents:
            recipients = contents["recipients"]
        else:
            recipients = None
       
        db["channels"].upsert({
            "id": int(channel_id),
            "type": channel_type,
            "name": channel_names[channel_id],
            "recipients": recipients,
            "guild_id": guild_id,
        }, 
            foreign_keys=[("guild_id", "servers", "id")],
            pk="id", 
            column_order=("id", "type", "name", "recipients", "guild_id")
        )
