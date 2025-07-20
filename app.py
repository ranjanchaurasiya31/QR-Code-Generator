from flask import Flask, render_template, request, send_file
import qrcode
import io
from PIL import Image
import qrcode.image.svg

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_data = None
    qr_format = 'png'
    if request.method == 'POST':
        qr_data = request.form.get('qrtext')
        qr_format = request.form.get('format', 'png').lower()
        if qr_data:
            return render_template('index.html', qr_data=qr_data, qr_format=qr_format)
    return render_template('index.html', qr_data=None, qr_format=qr_format)

@app.route('/qr_code')
def qr_code():
    qr_data = request.args.get('qr_data')
    qr_format = request.args.get('format', 'png').lower()
    if not qr_data:
        return '', 400
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    if qr_format == 'svg':
        img = qrcode.make(qr_data, image_factory=qrcode.image.svg.SvgImage)
        img.save(buf)
        buf.seek(0)
        return send_file(buf, mimetype='image/svg+xml')
    elif qr_format == 'jpg':
        img = img.convert('RGB')
        img.save(buf, format='JPEG')
        buf.seek(0)
        return send_file(buf, mimetype='image/jpeg')
    else:  # default to PNG
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')

@app.route('/download_qr')
def download_qr():
    qr_data = request.args.get('qr_data')
    qr_format = request.args.get('format', 'png').lower()
    if not qr_data:
        return '', 400
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    filename = f'qr_code.{qr_format}'
    if qr_format == 'svg':
        img = qrcode.make(qr_data, image_factory=qrcode.image.svg.SvgImage)
        img.save(buf)
        buf.seek(0)
        return send_file(buf, mimetype='image/svg+xml', as_attachment=True, download_name=filename)
    elif qr_format == 'jpg':
        img = img.convert('RGB')
        img.save(buf, format='JPEG')
        buf.seek(0)
        return send_file(buf, mimetype='image/jpeg', as_attachment=True, download_name=filename)
    else:  # default to PNG
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True) 