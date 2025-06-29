from flask import Flask,request,send_file , render_template
from PIL import Image
app=Flask(__name__)
import io

A4_SIZE = (595, 842)  # Format A4 en points (72dpi)

@app.route('/')
@app.route('/hello')
def display():
    return render_template("convertisseur.html")
@app.route('/convert', methods=['POST'])
def convert_images():
    images = request.files.getlist('images')
    processed_images = []

    for img_file in images:
        img = Image.open(img_file).convert("RGB")

        page = Image.new("RGB", A4_SIZE, "white")

        # Respecter les proportions sans perte de qualité
        scale = min((A4_SIZE[0] - 40) / img.width, (A4_SIZE[1] - 40) / img.height, 1)
        new_size = (int(img.width * scale), int(img.height * scale))

        if scale < 1:
            img = img.resize(new_size, Image.LANCZOS)

        pos_x = (A4_SIZE[0] - img.width) // 2
        pos_y = (A4_SIZE[1] - img.height) // 2
        page.paste(img, (pos_x, pos_y))

        processed_images.append(page)

    if not processed_images:
        return "Aucune image reçue", 400

    pdf_bytes = io.BytesIO()
    processed_images[0].save(pdf_bytes, format='PDF', save_all=True, append_images=processed_images[1:])
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name="converted.pdf", as_attachment=True, mimetype="application/pdf")


if __name__=="__main__":
    app.run(debug=True)