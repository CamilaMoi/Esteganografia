from PIL import Image

def converterBinario(mensagemUsuario):
    binarios = [format(ord(c), '08b') for c in mensagemUsuario]
    print(binarios)
    return binarios

def modificarPixels(pix, texto):
    """Modifies pixel values to encode the binary data."""
    textoBinario = converterBinario(texto)
    tamanhoTexto = len(textoBinario) #lendata vira tamanhotexto
    imdata = iter(pix) #cria um iterador sobre os pixels 
    
    for i in range(tamanhoTexto): #iterando sobre cada pixel na imagem que tem 9 valores
        pixels = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
        
        # modificar os valores dos pixels no LSB
        for j in range(8):
            if textoBinario[i][j] == '0' and pixels[j] % 2 != 0:
                pixels[j] -= 1
            elif textoBinario[i][j] == '1' and pixels[j] % 2 == 0:
                pixels[j] += 1
        
        # Set termination flag (last pixel even means continue, odd means stop)
        if i == tamanhoTexto - 1: #se ja estiver no 8 caractere dos bits, vai parar 
            pixels[-1] |= 1  # Make odd (stop flag)
        else:
            pixels[-1] &= ~1  # Make even (continue flag)
        
        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

def esconderTexto(imagem, texto):
    """Encodes the modified pixel data into the new image."""
    w = imagem.size[0]
    (x, y) = (0, 0)
    
    for pixel in modificarPixels(imagem.getdata(), texto): #coloca o texto na imagem 
        imagem.putpixel((x, y), pixel)
        x = 0 if x == w - 1 else x + 1
        y += 1 if x == 0 else 0

def codificar():
    img = input("nome da imagem (com extensão): ")
    image = Image.open(img, 'r')
    # Converter para RGB para garantir compatibilidade
    if image.mode != 'RGB':
        image = image.convert('RGB')
    texto = input("Insira o texto: ")
    
    if not texto:
        raise ValueError("texto vazio")
    
    newimg = image.copy()
    esconderTexto(newimg, texto)
    new_img_name = input("nome da nova imagem (com extensão) ")
    
    # Mapear formatos comuns para os formatos aceitos pelo PIL
    formato = new_img_name.split(".")[-1].upper()
    formato_map = {'JPG': 'JPEG', 'JPE': 'JPEG'}
    formato = formato_map.get(formato, formato)
    
    # Aviso sobre JPEG: formato com perda pode corromper a esteganografia
    if formato == 'JPEG':
        print("AVISO: JPEG é um formato com perda e pode corromper a esteganografia.")
        print("Recomendado usar PNG para preservar os valores exatos dos pixels.")
    
    newimg.save(new_img_name, formato)

def decodificar():
    img = input("nome da imagem (com extensão): ")
    image = Image.open(img, 'r')
    # Converter para RGB para garantir compatibilidade
    if image.mode != 'RGB':
        image = image.convert('RGB')
    imgdata = iter(image.getdata())
    data = ""
    
    while True:
        pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
        binstr = ''.join(['1' if i % 2 else '0' for i in pixels[:8]])
        data += chr(int(binstr, 2))
        
        if pixels[-1] % 2 != 0:
            break
    
    return data

def main():
    opcao = input(":: Escolha uma opção ::\n1. Encode\n2. Decode\n")
    if opcao == '1':
        codificar()
    elif opcao == '2':
        print("Decoded Word: " + decodificar())
    else:
        print("opcao invalida")

if __name__ == "__main__":
    main()