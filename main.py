import openpyxl as openpyxl
from PIL import Image, ImageDraw, ImageFont
import os
from bot import WhatsappBot
from argparse import ArgumentParser
import sys

def parse_args():
    parser = ArgumentParser(description='Bot para enviar cartões personalizados pelo whatsapp')
    parser.add_argument('-e', dest='excelFile', help='Arquivo excel com os nomes dos contatos e números')
    parser.add_argument('-c', dest='image', help='Imagem padrão do cartão (Modelo)')
    parser.add_argument('-m', dest='mensagem', help='Mensagem inicial enviada antes da foto')
    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    arguments = parser.parse_args()
    return arguments

def main():
    args = parse_args()
    # Imagem
    imagem = args.image

    # Instancia o bot com a mensagem padrão
    bot = WhatsappBot(args.mensagem)

    # Abre a planilha (Workbook) com os nomes e numeros dos contatos
    wb = openpyxl.load_workbook(filename=args.excelFile, read_only=True)

    # Seleciona a WorkSheet Contatos
    ws = wb['Contatos']

    # Cria uma instancia da ImageFont para escrever na imagem
    font = ImageFont.truetype("./Winter Wind.ttf", size=150)

    # Path do aplicativo
    path = os.path.dirname(os.path.abspath(__file__))

    # Loop na Worksheet a partir da linha 2 e coluna máxima 2, somente valores
    for row in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        try:
            # Instancia a imagem
            imagem = Image.open(imagem).convert("RGBA")

            # Cria o objeto ImageDraw
            lapis = ImageDraw.Draw(imagem)

            # Escreve o nome do contato na imagem
            lapis.text(
                (550, 756),
                text=f"{row[0]}",
                fill="#fae38f",
                anchor="ms",
                font=font
            )
            # Cria o nome amigável para o nome da imagem
            nameSplited = "_".join(row[0].lower().split())

            # Cria o padrão do nome cartao_nome_do_contato.png
            imageName = f"cartao_{nameSplited}.png"

            # Salva a imagem
            imagem.save("./%s"%imageName)

            # Ajuste para colocar +55 antes do número de telefone
            telNumber = "+55%s" % (row[1])

            # Pega o full path da imagem
            fullImagePath = os.path.join(path, imageName)

            # Abre para buscar o contato e verifica se conseguiu executar
            continueExecution = bot.buscarContato(telNumber)

            if continueExecution:
                # Se retornou true envia mensagem
                bot.enviarMensagem()

                # Se retornou true envia a imagem
                bot.enviarImagem(fullImagePath)

                # Se retornou true fecha a mensagem
                bot.fecharMsg()
            else:
                # Se retornou false imprime o erro
                print(F"Houve algum erro ao enviar para o contato {telNumber}")

        except Exception as e:
            # Se aconteceu um erro imprime o erro
            print(f"Error: {e}")


if __name__ == "__main__":
    main()


