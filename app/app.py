print("Hello1 world1")

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template

@app.route("/data_to")
def data_to():
    some_pars = {'user':'John','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 11

    return render_template('simple.html',some_str = some_str,some_value = some_value,some_pars=some_pars)

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, FloatField
# модули валидации полей формы
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта Google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ldcq70rAAAAAIUp2k7W8lDrKbPVo5fjR82nfetG' #'6Ld0O70rAAAAAGiF5PNP8VfteqQBA-RAufUJA8jx'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ldcq70rAAAAAPcm_d-IMskcQVNCUgAytnRekZFJ' #'6Ld0O70rAAAAADWpqM01w6D-bbLSTXzMLHIGSNeL'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap

#from bootstrap_flask import Bootstrap4
bootstrap = Bootstrap(app)

# создаем форму для загрузки файла
class NetForm(FlaskForm):
    # поле для введения строки, валидируется наличием данных
    # валидатор проверяет введение данных после нажатия кнопки submit
    # и указывает пользователю ввести данные, если они не введены
    # или неверны
    #openid = StringField('openid', validators = [DataRequired()])
    
    # поле загрузки файла
    # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()

    angle = FloatField('Rotation angle (degrees)', validators = [DataRequired(message="Angle is required"),NumberRange(min=-360, max=360, message="Angle must be between -360 and 360 degrees")])

    #кнопка submit, для пользователя отображена как send
    submit = SubmitField('Send')

# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os

# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet
# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
    # создаем объект формы
    form = NetForm()
    # обнуляем переменные, передаваемые в форму
    filename=None
    neurodic = {}
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
    # файлы с изображениями читаются из каталога static
        f = form.upload.data
        print(f"source filename : {f.filename}")
        filename = os.path.join('./static', secure_filename(f.filename))
        print(f"filename : {filename}")
        f.save(filename)
        angle = form.angle.data
        print(f"angle : {angle}")
        fimage = neuronet.read_image_file(filename,angle)
        fimage.save("./static/result.png")
        # передаем все изображения в каталоге на классификацию
        # можете изменить немного код и передать только загруженный файл
        ## decode = neuronet.getresult(fimage)
        # записываем в словарь данные классификации
        # for elem in decode:
        #     neurodic[elem[0][1]] = elem[0][2]
            # сохраняем загруженный файл
            #form.upload.data.save(filename)
        # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
        # сети, если был нажат сабмит, либо передадим falsy значения
    return render_template('net.html',form=form,image_name="./static/result.png",neurodic=neurodic)

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
# метод для обработки запроса от пользователя
@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
    neurodic = {}
    # проверяем, что в запросе json данные
    if request.mimetype == 'application/json':
        # получаем json данные
        data = request.get_json()
        # берем содержимое по ключу, где хранится файл
        # закодированный строкой base64
        # декодируем строку в массив байт, используя кодировку utf-8
        # первые 128 байт ascii и utf-8 совпадают, потому можно
        filebytes = data['imagebin'].encode('utf-8')
        # декодируем массив байт base64 в исходный файл изображение
        cfile = base64.b64decode(filebytes)
        # чтобы считать изображение как файл из памяти, используем BytesIO
        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)
        # пример сохранения переданного файла
        # handle = open('./static/f.png','wb')
        # handle.write(cfile)
        # handle.close()
        # преобразуем словарь в json-строку
        ret = json.dumps(neurodic)
        # готовим ответ пользователю
        resp = Response(response=ret,
        status=200,
        mimetype="application/json")
        # возвращаем ответ
        return resp

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
