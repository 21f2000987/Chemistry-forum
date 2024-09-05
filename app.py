from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# Mock database of blog posts
posts = [
    {'id': 1, 'title': 'The Importance of Chemical Reactions', 'content': 'A discussion on why chemical reactions are crucial in chemistry.', 'comments': []},
    {'id': 2, 'title': 'Chemical Kinetics', 'content': 'An overview of reaction rates and the Arrhenius Equation.', 'comments': []},
    {'id': 3, 'title': 'Chemical Equilibrium', 'content': 'An explanation of reversible reactions and equilibrium concepts.', 'comments': []},
    {'id': 4, 'title': 'Organic Mechanisms', 'content': 'A discussion on mechanisms in organic chemistry.', 'comments': []},
    {'id': 5, 'title': 'Organic Conversions', 'content': 'A review of various organic conversions and reactions.', 'comments': []}
]

# List of unlawful words (example list)
UNLAWFUL_WORDS = ['badword1', 'badword2', 'inappropriate']  # Replace with actual words

def is_valid_content(content):
    # Convert content to lowercase to make the check case-insensitive
    content_lower = content.lower()
    # Check for any unlawful words
    for word in UNLAWFUL_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', content_lower):
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return render_template('404.html'), 404  # Handle post not found
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/discussion', methods=['GET', 'POST'])
def discussion(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return render_template('404.html'), 404  # Handle post not found
    
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        
        if is_valid_content(comment):
            post['comments'].append({'name': name, 'text': comment})
            return redirect(url_for('discussion', post_id=post_id))
        else:
            flash('Your comment contains unlawful or invalid content and could not be posted.')
    
    return render_template('discussion.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/comment/<int:comment_index>/delete', methods=['POST'])
def delete_comment(post_id, comment_index):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post and 0 <= comment_index < len(post['comments']):
        post['comments'].pop(comment_index)
    return redirect(url_for('discussion', post_id=post_id))

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        content = request.form['content']
        
        if is_valid_content(title) and is_valid_content(content):
            if posts:
                new_id = max(post['id'] for post in posts) + 1
            else:
                new_id = 1
            
            posts.append({'id': new_id, 'title': title, 'content': content, 'comments': []})
            return redirect(url_for('index'))
        else:
            flash('The title or content contains unlawful or invalid words and could not be posted.')
    
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
