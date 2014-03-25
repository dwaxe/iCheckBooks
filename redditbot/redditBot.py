import praw
import re

# Matches all non-alphanumerics
pattern = re.compile('[\W_\]+')

# Import the list of books {title: upvotes}
bookData = {'i am america and so can you': 0, 'the catcher in the rye': 0,
'the great gatsby': 0, 'slaughterhouse five': 0, 'siddhartha': 0, 'frozen': 0}


# Create the Reddit object
r = praw.Reddit(user_agent='reader')
# Log in
r.login('iCheckBooks', 'icheckb00ks')
# Create list of already checked submissions
already_done = []

# Strip all non-alphanumeric characters and set to lower case
def normalizeText(text):
	return pattern.sub('', text).lower()

# If the text discusses a book, add the thing's ups
def bookInThing(thing, text):
	has_book = any(string in text for string in bookData)
	print('doin that thang')
	if thing.id not in already_done and has_book:
		already_done.append(thing.id)
		# Loop through the book titles and add ups
		for title in bookData:
			if title in text:
				bookData[title] += thing.ups

# Main loop
while True:
	# Create subreddit object
	subreddit = r.get_subreddit('books')
	# Loop through the hottest ten submissions
	for submission in subreddit.get_hot(limit=10):
		# If the selftext or title discusses a book, add the submission upvotes
		bookInThing(submission, submission.selftext.lower() + submission.title.lower())
		# If the comment discusses a book, add the comment ups
		comments = praw.helpers.flatten_tree(submission.comments)
		# Length-2 because the last object is not a comment
		for comment in comments:
			if not isinstance(comment, praw.objects.Comment):
				continue
			bookInThing(comment, comment.body.lower())
	break



# Spam Filburt_Turtle with messages
r.send_message('Filburt_Turtle', '[Books and Scores]', str(bookData))


# At this point, update the database with the new upvote values
