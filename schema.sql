CREATE TABLE users(
  id integer not null primary key,
  reputation int not null,
  views int not null,
  upvotes int not null,
  downvotes int not null,
  creation_date text not null,
  display_name text not null,
  image_url text not null,
  last_access_date text not null,
  location text not null,
  about_me text not null,
  email_hash text not null
);

CREATE TABLE badges(
  id integer not null primary key,
  user_id int not null references users(id),
  name text not null,
  date text not null
);

CREATE TABLE posts(
  id integer not null primary key,
  post_type text not null check (post_type in ('question', 'answer', 'wiki', 'tag-wiki-excerpt', 'tag-wiki', 'moderation-nomination', 'wiki-placeholder', 'privilege-wiki')),
  score int not null,
  views int not null,
  answers int not null,
  comments int not null,
  favorites int not null,
  creation_date text not null,
  closed_date text,
  accepted_answer_id int references posts(id),
  parent_id int references posts(id),
  owner_user_id int references users(id),
  community_owned_date text,
  tags text,
  title text,
  body text not null,
  last_editor_user_id int references users(id),
  last_edit_date text,
  last_activity_date text not null
);

CREATE TABLE votes(
  id integer not null primary key,
  post_id int not null references posts(id),
  -- CONSIDER: translate vote_type_id ?
  vote_type text not null check (vote_type in ('accepted', 'up', 'down', 'offensive', 'favorite', 'close', 'reopen', 'bounty-start', 'bounty-close', 'delete', 'undelete', 'spam', 'mod-view-flagged', 'edit-approved')),
  creation_date text not null,
  user_id int references users(id),
  bounty_amount int
);

CREATE TABLE comments(
  id integer not null primary key,
  post_id int not null references posts(id),
  user_id int not null references users(id),
  creation_date text not null,
  score int not null,
  text text not null
);

CREATE VIEW questions AS
SELECT
  id,
  score,
  views,
  answers,
  comments,
  favorites,
  creation_date,
  closed_date,
  accepted_answer_id,
  owner_user_id,
  community_owned_date,
  tags,
  title,
  body,
  last_editor_user_id,
  last_edit_date,
  last_activity_date
FROM posts WHERE post_type = 'question';

CREATE VIEW answers AS
SELECT
  id,
  score,
  comments,
  creation_date,
  parent_id,
  owner_user_id,
  community_owned_date,
  body,
  last_editor_user_id,
  last_edit_date,
  last_activity_date
FROM posts WHERE post_type = 'answer';

