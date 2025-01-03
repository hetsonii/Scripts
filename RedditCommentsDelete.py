import praw

# Reddit API credentials
client_id = '<REDACTED>'
client_secret = '<REDACTED>'
username = '<REDACTED>'
password = '<REDACTED>'
user_agent = 'Comment Deleter/v1.0 by <REDACTED>'

# Words to search for in comments
words_to_search = ['<REDACTED>']

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Fetch and delete comments containing specific words
for comment in reddit.user.me().comments.new(limit=None):
    for word in words_to_search:
        if word.lower() in comment.body.lower():
            print(f"Deleting comment with ID: {comment.id}")
            comment.delete()
            break  # Stop searching if deleted

print("All comments containing specified words have been deleted.")
