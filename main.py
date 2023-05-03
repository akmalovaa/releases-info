import os
from flask import Flask, request, render_template, send_file, send_from_directory, url_for
# from image_generator import generate_image
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # handle the POST request
    context = ''
    # if request.method == 'POST':
    #     image_size = int(request.form.get('image_size'))
    #     image_type = str(request.form.get('image_type'))
    #     if image_size > 0 and image_size < 999:
    #         generate_image(int(image_size), str(image_type))
    #         download_url = f"{url_for('index', _external=True)}downloads/{image_size}.{image_type}"
    #         context = {'size' : image_size, 'format' : image_type, 'url' : download_url}
    #     else:
    #         context = 'Error'
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)