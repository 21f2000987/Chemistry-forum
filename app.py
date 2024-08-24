from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock database
posts = [
    {'id': 1, 'title': 'The Importance of Chemical Reactions', 'content': 'Discussion on why chemical reactions are crucial in chemistry.', 'comments': []},
    {'id': 2, 'title': 'Chemical Kinetics', 'content': 'Rate and Arhennius Equation.', 'comments': []},
    {'id': 3, 'title': 'Chemical Equilibirium', 'content': 'Reversible Reactions.', 'comments': []},
    {'id': 4, 'title': 'Organic Mechanisms', 'content': 'Discuss.', 'comments': []},
    {'id': 5, 'title': 'Organic Conversions', 'content': 'Discuss.', 'comments': []}
]


@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/discussion', methods=['GET', 'POST'])
def discussion(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        post['comments'].append({'name': name, 'text': comment})
        return redirect(url_for('discussion', post_id=post_id))
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
        
        # Generate new ID
        if posts:
            new_id = max(post['id'] for post in posts) + 1
        else:
            new_id = 1  # Start with ID 1 if the list is empty
        
        posts.append({'id': new_id, 'title': title, 'content': content, 'comments': []})
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
