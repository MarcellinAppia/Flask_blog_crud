from flask import Flask,render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    
def __repr__(self):
    return '<Blog %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

@app.route('/blog', methods=['GET','POST'])
def blog():
    if request.method == 'GET':
        articles = Article.query.order_by(Article.created_at).all()
        
    return render_template('blog.html', articles = articles)

@app.route('/blog/newblog', methods=['GET','POST'])
def newArticle():
    if request.method == 'POST':
        titre = request.form['titre']
        content = request.form['article']
        new_article = Article(title = titre, content = content)
        
        try:
            db.session.add(new_article)
            db.session.commit()
            return redirect('/blog')
            
        except:
            return 'Une erreur inattendue'
    return render_template('newblog.html')

@app.route('/supprimer/<int:id>')
def supprimer(id):
    post_a_supprimer = Article.query.get_or_404(id)
    
    try:
        db.session.delete(post_a_supprimer)
        db.session.commit()
        return redirect('/blog')
    except:
        return 'un probleme est survenue lors de la suppression'
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    post_to_update = Article.query.get_or_404(id)
    if request.method == 'POST':
        
        post_to_update.title = request.form['titre']
        post_to_update.content = request.form['article']
        post_to_update.created_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return redirect('/blog')
        except:
            return 'une erreur est survenue lors de la modification'
    else:
        return render_template('update.html', post_to_update=post_to_update)
        