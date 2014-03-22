# Python script to help explore PRAW
import praw

r = praw.Reddit(user_agent='prawhelper')

r.login('iCheckBooks', 'icheckb00ks')

subreddit = r.get_subreddit('books')

submissions = subreddit.get_top(limit=10)

submission = next(submissions)

comments = praw.helpers.flatten_tree(submission.comments)

comment = comments[0]
