CREATE INDEX idx_badges_user_id ON badges(user_id);

CREATE INDEX idx_posts_owner_user_id ON posts(owner_user_id);
CREATE INDEX idx_posts_last_editor_user_id ON posts(last_editor_user_id);
CREATE INDEX idx_posts_accepted_answer_id ON posts(accepted_answer_id) WHERE accepted_answer_id IS NOT NULL;
CREATE INDEX idx_posts_parent_id ON posts(parent_id) WHERE parent_id IS NOT NULL;

CREATE INDEX idx_votes_user_id ON votes(user_id);
CREATE INDEX idx_votes_post_id ON votes(post_id);

CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
