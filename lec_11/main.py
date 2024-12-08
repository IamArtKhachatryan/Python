import requests

def handle_response(response, success_code, success_message, error_message):
    if response.status_code == success_code:
        print(f"{success_message}: {response.json() if response.text else 'No Content'}")
        return response.json() if response.text else None
    else:
        print(f"{error_message} (HTTP {response.status_code}): {response.text}")
        return None


def create_post(data):

    try:
        response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
        result = handle_response(
            response,
            success_code=201,
            success_message="Post successfully created",
            error_message="Failed to create post"
        )
        return result['id'] if result else None
    except requests.RequestException as e:
        print(f"Error creating post: {e}")
        return None


def update_post(post_id, data):

    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    try:
        response = requests.put(url, json=data)
        handle_response(
            response,
            success_code=200,
            success_message="Post successfully updated",
            error_message="Failed to update post"
        )
    except requests.RequestException as e:
        print(f"Error updating post: {e}")


def delete_post(post_id):

    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    try:
        response = requests.delete(url)
        handle_response(
            response,
            success_code=200,
            success_message="Post successfully deleted",
            error_message="Failed to delete post"
        )
    except requests.RequestException as e:
        print(f"Error deleting post: {e}")


def get_filtered_posts():

    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        if response.status_code == 200:
            posts = response.json()

            # Filter posts by title length
            filtered_by_titles = [post for post in posts if len(post['title'].split()) > 6][:6]
            print("\nFiltered Posts by Title Length (> 6 words):")
            for post in filtered_by_titles:
                print(f" - {post['title']}")

            # Filter posts by body newline count
            filtered_by_body = [post for post in posts if post['body'].count('\n') > 2][:3]
            print("\nFiltered Posts by Body Newline Count (> 2 newlines):")
            for post in filtered_by_body:
                print(f" - {post['body']}")
        else:
            print(f"Failed to fetch posts (HTTP {response.status_code})")
    except requests.RequestException as e:
        print(f"Error fetching posts: {e}")


# Main execution
if __name__ == "__main__":
    data = {
        'title': 'Example Post',
        'body': 'This is an example body of the post.',
        'userId': 1
    }

    post_id = create_post(data)

    if post_id:
        updated_data = {
            'title': 'Updated Post Title',
            'body': 'Updated post body with additional information.',
            'userId': 1
        }
        update_post(post_id, updated_data)

        delete_post(post_id)

    get_filtered_posts()
