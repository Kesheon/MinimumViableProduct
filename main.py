from flask import Flask, url_for, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)



#Views
#-----
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
