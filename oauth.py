import pytumblr
from urllib.parse import parse_qs

client = pytumblr.TumblrRestClient(
  'UrxF3SVrbG8Hrcy6MCzqfqOUWwypa8juv2MmoWCgU793NYxZdK',
  '7gaCuJB16nJpXbJySm6DOaXdnAEvEm6AzSJRPaz3cJnxCc619T',
  'B1xgVQ4YgXDA8KoSWIaz7l1syOsHPzKgobAnKwAWQUwTT68OIE',
  '2gi6zLMGvjvFkh7OJHC39LfwnStNQVEn9622Wjt0tgoMzEm8Ih'
)

# Make the request
response = client.likes()
for i in response['liked_posts']:
    print(i['post_url'])