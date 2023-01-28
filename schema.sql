CREATE TABLE users(
  id int primary key,
  reputation int not null,
  creation_date text not null,
  display_name text not null,
  email_hash text not null,
  last_access_date text not null,
  location text not null,
  about_me text not null,
  views int not null,
  upvotes int not null,
  downvotes int not null
);

CREATE TABLE badges(
  id int primary key,
  user_id int not null references users(id),
  name text not null,
  date text not null
);

CREATE TABLE posts(
  id int primary key,
  post_type text not null check (post_type in ('question', 'answer', 'wiki', 'tag-wiki-excerpt', 'tag-wiki', 'moderation-nomination', 'wiki-placeholder', 'privilege-wiki')),
  accepted_answer_id int references posts(id),
  parent_id int references posts(id),
  creation_date text not null,
  community_owned_date text,
  closed_date text,
  score int not null,
  view_count int not null,
  body text not null,
  owner_user_id int,
  last_editor_user_id int,
  last_editor_display_name text,
  last_edit_date text,
  last_activity_date text not null,
  title text,
  tags text,
  answer_count int not null,
  comment_count int not null,
  favorite_count int not null
);

CREATE TABLE votes(
  id int primary key,
  post_id int not null references posts(id),
  -- CONSIDER: translate vote_type_id ?
  vote_type text not null check (vote_type in ('accepted', 'up', 'down', 'offensive', 'favorite', 'close', 'reopen', 'bounty-start', 'bounty-close', 'delete', 'undelete', 'spam', 'mod-view-flagged', 'edit-approved')),
  creation_date text not null,
  user_id int references users(id),
  bounty_amount int
);

CREATE TABLE comments(
  id int primary key,
  post_id int not null references posts(id),
  score int not null,
  text text not null,
  creation_date text not null,
  user_id int not null references uesrs(id)
);

-- TODO: views for questions and answers
