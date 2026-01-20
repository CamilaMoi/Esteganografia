# Esteganografia de Imagens - LSB (Least Significant Bit)

Projeto de implementação de esteganografia usando a técnica LSB (Least Significant Bit) para esconder uma imagem dentro de outra imagem.

##  O que é Esteganografia?

Esteganografia é a arte e ciência de esconder informações dentro de outros arquivos, de forma que a existência da mensagem secreta não seja detectada. Diferente da criptografia, que torna a mensagem ilegível mas visível, a esteganografia torna a mensagem invisível.

### Como Funciona Esta Implementação

Esta implementação utiliza a técnica **LSB (Least Significant Bit)** para esconder uma imagem secreta dentro de uma imagem "cover" (capa). O método funciona da seguinte forma:

1. **Conversão para Binário**: A imagem secreta é convertida para uma sequência de bits, incluindo suas dimensões (largura e altura).

2. **Modificação dos Pixels**: Os bits menos significativos (LSB) dos pixels da imagem cover são modificados para armazenar os bits da imagem secreta. Como apenas o bit menos significativo é alterado, a mudança visual é praticamente imperceptível ao olho humano.

3. **Estrutura de Dados**:
   - **32 bits iniciais**: Armazenam as dimensões da imagem secreta (16 bits para largura + 16 bits para altura)
   - **Restante dos bits**: Armazenam os dados RGB de cada pixel da imagem secreta (24 bits por pixel: 8 para R, 8 para G, 8 para B)

4. **Flag de Parada**: O 9º valor RGB de cada grupo de 3 pixels é usado como flag para indicar quando a mensagem termina (ímpar = parar, par = continuar).

### Capacidade de Armazenamento

- Cada grupo de **3 pixels da imagem cover** pode esconder **8 bits** de informação
- Cada pixel RGB da imagem secreta requer **9 pixels da imagem cover** (24 bits ÷ 8 bits por grupo × 3 pixels por grupo)
- As dimensões requerem **12 pixels adicionais** (32 bits ÷ 8 bits por grupo × 3 pixels por grupo)

**Fórmula**: `pixels_necessarios = (pixels_imagem_secreta × 9) + 12`

##  Pré-requisitos

### Software Necessário

- **Python 3.6 ou superior**
- **Pillow (PIL)** - Biblioteca para manipulação de imagens

### Instalação das Dependências

```bash
pip install Pillow
```

### Formato de Imagens

- **Recomendado**: PNG (formato sem perda, preserva os valores exatos dos pixels)
- **Não recomendado**: JPEG/JPG (formato com perda, pode corromper a esteganografia devido à compressão)

##  Como Usar

### Executar o Programa

```bash
python esteganografia.py
```

### Codificar (Esconder Imagem)

1. Execute o programa e escolha a opção `1` (Encode)
2. Informe o nome da **imagem cover** (onde esconder, com extensão)
   - Exemplo: `cover.png`
3. Informe o nome da **imagem secreta** (o que esconder, com extensão)
   - Exemplo: `hidden.png`
4. Informe o nome da **nova imagem codificada** (com extensão)
   - Exemplo: `imagem_codificada.png`

**Importante**: A imagem cover deve ser grande o suficiente para esconder a imagem secreta. O programa verificará automaticamente e informará se a imagem cover é muito pequena.

### Decodificar (Extrair Imagem)

1. Execute o programa e escolha a opção `2` (Decode)
2. Informe o nome da **imagem codificada** (com extensão)
   - Exemplo: `imagem_codificada.png`
3. Informe o nome da **imagem extraída** (com extensão)
   - Exemplo: `imagem_extraida.png`

### Exemplo de Uso Completo

```bash
$ python esteganografia.py
:: Escolha uma opção ::
1. Encode (Esconder imagem)
2. Decode (Extrair imagem)
1
nome da imagem cover (onde esconder, com extensão): cover.png
nome da imagem secreta (o que esconder, com extensão): hidden.png
nome da nova imagem (com extensão): resultado.png
Imagem codificada salva como resultado.png
```

##  Limitações e Considerações

1. **Formato JPEG**: Não é recomendado usar JPEG devido à compressão com perda, que pode corromper a mensagem escondida.

2. **Tamanho da Imagem Cover**: A imagem cover deve ser significativamente maior que a imagem secreta. Use a fórmula acima para calcular o tamanho mínimo necessário.

3. **Qualidade Visual**: Embora as alterações sejam mínimas, imagens muito pequenas ou com muitas cores podem mostrar pequenas diferenças visuais.

4. **Segurança**: Esta é uma implementação educacional. Para uso em produção, considere técnicas adicionais de segurança e criptografia.

## 🔍 Como Funciona Tecnicamente

### Algoritmo de Codificação

1. Converte a imagem secreta para RGB se necessário
2. Extrai largura e altura (16 bits cada)
3. Converte cada pixel RGB para 24 bits (8 bits por canal)
4. Para cada grupo de 3 pixels da cover:
   - Modifica os 8 primeiros valores RGB (LSB) para armazenar 8 bits
   - Usa o 9º valor como flag de continuação/parada
5. Salva a imagem modificada

### Algoritmo de Decodificação

1. Lê os pixels da imagem codificada sequencialmente
2. Extrai os LSBs de cada grupo de 3 pixels
3. Reconstrói as dimensões (primeiros 32 bits)
4. Reconstrói os pixels RGB (24 bits por pixel)
5. Cria e salva a imagem secreta extraída

## Notas sobre Branches (Git)

Se você estiver usando controle de versão Git:

- **codificarImagem**: Branch com features de esconder imagens
- **codificarTexto**: Branch com feature de esconder texto 


##  Solução de Problemas

### Erro: "Imagem cover muito pequena"
- **Solução**: Use uma imagem cover maior ou reduza o tamanho da imagem secreta

### Erro: "Não há bits suficientes para decodificar"
- **Causa**: A imagem pode ter sido salva como JPEG ou corrompida
- **Solução**: Use sempre PNG para codificação e decodificação

### Imagem extraída aparece parcialmente preta
- **Causa**: A imagem foi salva como JPEG ou não há bits suficientes
- **Solução**: Certifique-se de usar PNG e que a imagem cover seja grande o suficiente
