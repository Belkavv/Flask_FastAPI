from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/about/')
def about():
    return 'about'

@app.route('/clothes/')
def clothes():
    return render_template('clothes.html')

@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')

@app.route('/jacket/')
def jackets():
    return render_template('jacket.html')

if __name__ == '__main__':
    app.run(debug=True)