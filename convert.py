#!/usr/bin/env python3
import os
import json
import sqlite3
import xml.etree.ElementTree as ET

def go():
    remove_old_db()

    conn = sqlite3.connect('stack.db')
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous = normal')


    create_schema(conn)

    import_users(conn)
    import_badges(conn)
    import_posts(conn)
    import_votes(conn)
    import_comments(conn)
    conn.commit()
    conn.close()


def remove_old_db():
    try:
        os.remove('stack.db')
    except FileNotFoundError:
        pass

def create_schema(conn):
    f = open('schema.sql')
    conn.executescript(f.read())
    f.close()

def timestamp(ts):
    # Switch from ISO8601 to SQL format
    return ts.replace('T', ' ')

def import_badges(conn):
    tree = ET.parse('input/badges.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO badges(id, user_id, name, date) VALUES (?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['UserId']),
                         attrs['Name'],
                         attrs['Date'],
                     ])


def import_users(conn):
    tree = ET.parse('input/users.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO users(id, reputation, creation_date, display_name, email_hash, last_access_date, location, about_me, views, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['Reputation']),
                         timestamp(attrs['CreationDate']),
                         attrs['DisplayName'],
                         attrs['EmailHash'],
                         timestamp(attrs['LastAccessDate']),
                         attrs.get('Location', ''),
                         attrs.get('AboutMe', ''),
                         int(attrs['Views']),
                         int(attrs['UpVotes']),
                         int(attrs['DownVotes']),
                     ])

def post_type(ptid):
    if ptid == 1: return 'question'
    if ptid == 2: return 'answer'
    if ptid == 3: return 'wiki'
    if ptid == 4: return 'tag-wiki-excerpt'
    if ptid == 5: return 'tag-wiki'
    if ptid == 6: return 'moderation-nomination'
    if ptid == 7: return 'wiki-placeholder'
    if ptid == 8: return 'privilege-wiki'
    raise Exception('unknown ptid {}'.format(ptid))

def tags(x):
    return json.dumps([tag.strip('>') for tag in x.split('<') if tag])

def import_posts(conn):
    tree = ET.parse('input/posts.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO posts(id, post_type, accepted_answer_id, parent_id, creation_date, community_owned_date, closed_date, score, view_count, body, owner_user_id, last_editor_user_id, last_editor_display_name, last_edit_date, last_activity_date, title, tags, answer_count, comment_count, favorite_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         post_type(int(attrs['PostTypeId'])),
                         int(attrs['AcceptedAnswerId']) if 'AcceptedAnswerId' in attrs else None,
                         int(attrs['ParentId']) if 'ParentId' in attrs else None,
                         timestamp(attrs['CreationDate']),
                         timestamp(attrs['CommunityOwnedDate']) if 'CommunityOwnedDate' in attrs else None,
                         timestamp(attrs['ClosedDate']) if 'ClosedDate' in attrs else None,
                         int(attrs['Score']),
                         int(attrs['ViewCount'] or '0'),
                         attrs['Body'],
                         int(attrs['OwnerUserId']) if 'OwnerUserId' in attrs else None,
                         int(attrs['LastEditorUserId']) if 'LastEditorUserId' in attrs else None,
                         attrs['LastEditorDisplayName'] if 'LastEditorDisplayName' in attrs else None,
                         timestamp(attrs['LastEditDate']) if 'LastEditDate' in attrs else None,
                         timestamp(attrs['LastActivityDate']),
                         attrs['Title'] if 'Title' in attrs else None,
                         tags(attrs['Tags']) if 'Tags' in attrs else None,
                         int(attrs['AnswerCount']) if 'AnswerCount' in attrs else 0,
                         int(attrs['CommentCount']) if 'CommentCount' in attrs else 0,
                         int(attrs['FavoriteCount']) if 'FavoriteCount' in attrs else 0,
                     ])

def vote_type(vtid):
    if vtid == 1: return 'accepted'
    if vtid == 2: return 'up'
    if vtid == 3: return 'down'
    if vtid == 4: return 'offensive'
    if vtid == 5: return 'favorite'
    if vtid == 6: return 'close'
    if vtid == 7: return 'reopen'
    if vtid == 8: return 'bounty-start'
    if vtid == 9: return 'bounty-close'
    if vtid == 10: return 'delete'
    if vtid == 11: return 'undelete'
    if vtid == 12: return 'spam'
    if vtid == 15: return 'mod-view-flagged'
    if vtid == 16: return 'edit-approved'

    raise Exception('unknown vtid {}'.format(vtid))

def import_votes(conn):
    tree = ET.parse('input/votes.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib
        cur = conn.execute('INSERT INTO votes(id, post_id, vote_type, creation_date, user_id, bounty_amount) VALUES (?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostId']),
                         vote_type(int(attrs['VoteTypeId'])),
                         timestamp(attrs['CreationDate']),
                         int(attrs['UserId']) if 'UserId' in attrs else None,
                         int(attrs['BountyAmount']) if 'BountyAmount' in attrs else None
                     ])


def import_comments(conn):
    tree = ET.parse('input/comments.xml')
    rows = tree.getroot()
    for row in rows:
        attrs = row.attrib

        # 487 of 19,651 rows lack a user id, skip em.
        if not 'UserId' in attrs:
            continue
        cur = conn.execute('INSERT INTO comments(id, post_id, score, text, creation_date, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                     [
                         int(attrs['Id']),
                         int(attrs['PostId']),
                         int(attrs.get('Score', 0)),
                         attrs['Text'],
                         timestamp(attrs['CreationDate']),
                         int(attrs['UserId']),
                     ])

if __name__ == '__main__':
    go()

