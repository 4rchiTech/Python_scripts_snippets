import qrcode


######################### CONSTANTES ###############################

# (LIEN à QR coder, nom fichier FINAL)
QR_SEANODE = ("https://website.example", "qr_website_example.png")

########## ATELIER ###############################


def generateur_qr_code(source=None):
    img = qrcode.make(source[0])
    type(img)  # qrcode.image.pil.PilImage
    return img.save(source[1])


generateur_qr_code(source=QR_SEANODE)
