from PIL import Image

def converterImagemParaBinario(imagem_secreta):
    """Converte a imagem secreta para uma lista de bits."""
    # Primeiro, converter para RGB se necessário
    if imagem_secreta.mode != 'RGB':
        imagem_secreta = imagem_secreta.convert('RGB')
    
    largura, altura = imagem_secreta.size
    pixels = list(imagem_secreta.getdata())
    
    # Converter dimensões para binário (16 bits cada = 2 bytes)
    largura_bin = format(largura, '016b')
    altura_bin = format(altura, '016b')
    
    # Converter cada pixel (RGB = 3 bytes = 24 bits) para binário
    dados_binarios = []
    
    # Adicionar largura e altura primeiro (32 bits total)
    dados_binarios.extend([bit for bit in largura_bin])
    dados_binarios.extend([bit for bit in altura_bin])
    
    # Adicionar todos os pixels
    for pixel in pixels:
        r, g, b = pixel
        # Converter cada componente RGB para 8 bits
        dados_binarios.extend([bit for bit in format(r, '08b')])
        dados_binarios.extend([bit for bit in format(g, '08b')])
        dados_binarios.extend([bit for bit in format(b, '08b')])
    
    return dados_binarios

def modificarPixelsImagem(pix, dados_binarios):
    """Modifica os pixels da imagem cover para esconder os dados binários."""
    imdata = iter(pix)
    total_bits = len(dados_binarios)
    bit_index = 0
    
    while bit_index < total_bits:
        # Pegar 3 pixels (9 valores RGB)
        pixels = []
        try:
            for _ in range(3):
                pixel = next(imdata)
                pixels.extend(list(pixel[:3]))
        except StopIteration:
            # Se não houver mais pixels, parar o gerador
            # Não fazer yield se não temos 9 valores
            break
        
        # Verificar se temos 9 valores antes de processar
        if len(pixels) != 9:
            break
        
        # Modificar os 8 primeiros valores (LSB) para esconder os bits
        for j in range(8):
            if bit_index < total_bits:
                bit = dados_binarios[bit_index]
                if bit == '0' and pixels[j] % 2 != 0:
                    pixels[j] -= 1
                elif bit == '1' and pixels[j] % 2 == 0:
                    pixels[j] = pixels[j] - 1 if pixels[j] != 0 else pixels[j] + 1
                bit_index += 1
        
        # Usar o 9º pixel como flag de continuação
        if bit_index >= total_bits:
            pixels[-1] |= 1  # Make odd (stop flag)
        else:
            pixels[-1] &= ~1  # Make even (continue flag)
        
        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

def esconderImagem(imagem_cover, imagem_secreta):
    """Esconde a imagem secreta na imagem cover."""
    dados_binarios = converterImagemParaBinario(imagem_secreta)
    w = imagem_cover.size[0]
    (x, y) = (0, 0)
    
    for pixel in modificarPixelsImagem(imagem_cover.getdata(), dados_binarios):
        imagem_cover.putpixel((x, y), pixel)
        x = 0 if x == w - 1 else x + 1
        y += 1 if x == 0 else 0

def codificar():
    img_cover = input("nome da imagem cover (onde esconder, com extensão): ")
    imagem_cover = Image.open(img_cover, 'r')
    if imagem_cover.mode != 'RGB':
        imagem_cover = imagem_cover.convert('RGB')
    
    img_secreta = input("nome da imagem secreta (o que esconder, com extensão): ")
    imagem_secreta = Image.open(img_secreta, 'r')
    if imagem_secreta.mode != 'RGB':
        imagem_secreta = imagem_secreta.convert('RGB')
    
    # Verificar se a imagem cover é grande o suficiente
    cover_pixels = imagem_cover.size[0] * imagem_cover.size[1]
    secreta_pixels = imagem_secreta.size[0] * imagem_secreta.size[1]
    # Cada pixel da imagem secreta precisa de 3 pixels da cover (24 bits / 8 bits por pixel = 3)
    # Mais 32 bits para largura e altura = 4 pixels adicionais
    pixels_necessarios = (secreta_pixels * 3) + 4
    
    if cover_pixels < pixels_necessarios:
        raise ValueError(f"Imagem cover muito pequena! Precisa de pelo menos {pixels_necessarios} pixels, mas tem apenas {cover_pixels}")
    
    newimg = imagem_cover.copy()
    esconderImagem(newimg, imagem_secreta)
    new_img_name = input("nome da nova imagem (com extensão): ")
    
    # Mapear formatos comuns para os formatos aceitos pelo PIL
    formato = new_img_name.split(".")[-1].upper()
    formato_map = {'JPG': 'JPEG', 'JPE': 'JPEG'}
    formato = formato_map.get(formato, formato)
    
    newimg.save(new_img_name, formato)
    print(f"Imagem codificada salva como {new_img_name}")

def decodificar():
    img = input("nome da imagem codificada (com extensão): ")
    image = Image.open(img, 'r')
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    imgdata = iter(image.getdata())
    bits = []
    
    # Ler bits até encontrar o flag de parada
    while True:
        try:
            pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
        except StopIteration:
            # Se não houver mais pixels, parar a leitura
            break
        
        # Extrair os 8 primeiros bits
        for i in range(8):
            bits.append('1' if pixels[i] % 2 else '0')
        
        # Verificar flag de parada
        if pixels[-1] % 2 != 0:
            break
    
    # Converter bits para dados da imagem
    # Primeiros 16 bits = largura
    largura_bin = ''.join(bits[0:16])
    largura = int(largura_bin, 2)
    
    # Próximos 16 bits = altura
    altura_bin = ''.join(bits[16:32])
    altura = int(altura_bin, 2)
    
    # Resto dos bits = pixels da imagem (cada pixel = 24 bits = 3 bytes RGB)
    pixels_bits = bits[32:]
    total_pixels = largura * altura
    
    # Criar lista de pixels
    pixels_imagem = []
    for i in range(total_pixels):
        pixel_start = i * 24
        if pixel_start + 24 > len(pixels_bits):
            break
        
        # Extrair R, G, B (8 bits cada)
        r_bin = ''.join(pixels_bits[pixel_start:pixel_start+8])
        g_bin = ''.join(pixels_bits[pixel_start+8:pixel_start+16])
        b_bin = ''.join(pixels_bits[pixel_start+16:pixel_start+24])
        
        r = int(r_bin, 2)
        g = int(g_bin, 2)
        b = int(b_bin, 2)
        
        pixels_imagem.append((r, g, b))
    
    # Criar a imagem secreta
    imagem_secreta = Image.new('RGB', (largura, altura))
    imagem_secreta.putdata(pixels_imagem)
    
    nome_saida = input("nome da imagem extraída (com extensão): ")
    formato = nome_saida.split(".")[-1].upper()
    formato_map = {'JPG': 'JPEG', 'JPE': 'JPEG'}
    formato = formato_map.get(formato, formato)
    
    imagem_secreta.save(nome_saida, formato)
    print(f"Imagem secreta extraída e salva como {nome_saida}")
    return imagem_secreta

def main():
    opcao = input(":: Escolha uma opção ::\n1. Encode (Esconder imagem)\n2. Decode (Extrair imagem)\n")
    if opcao == '1':
        codificar()
    elif opcao == '2':
        decodificar()
    else:
        print("opcao invalida")

if __name__ == "__main__":
    main()