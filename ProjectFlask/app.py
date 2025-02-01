from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ключ для защиты форм
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Папка для загруженных файлов
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Создаем папку, если её нет


class PhotoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


@app.route('/')
def photo_list():
    photos = os.listdir(app.config['UPLOAD_FOLDER'])  # Получаем список файлов
    return render_template('photo_list.html', photos=photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        filename = secure_filename(image.filename)  # Безопасное имя файла
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Сохраняем файл
        flash(f'Photo "{title}" uploaded successfully!', 'success')
        return redirect(url_for('photo_list'))
    return render_template('upload_photo.html', form=form)


@app.route('/delete/<filename>', methods=['POST'])
def delete_photo(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)  # Удаляем файл
        flash(f'Photo "{filename}" deleted successfully!', 'success')
    else:
        flash(f'Photo "{filename}" not found!', 'danger')
    return redirect(url_for('photo_list'))


if __name__ == '__main__':
    app.run(debug=True)