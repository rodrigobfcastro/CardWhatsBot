import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WhatsappBot:
    def __init__(self, mensagem):
        # pega o path do programa
        dir_path = os.getcwd()

        # Junta o path com a pasta profile/wpp
        profile = os.path.join(dir_path, "profile", "wpp")

        # Cria as opções do webdriver
        chrome_options = webdriver.ChromeOptions()

        # Se existir o diretório de Profile do navegador, adiciona nas opções
        if os.path.isdir(profile):
            # Adiciona os argumentos as opções
            chrome_options.add_argument(
                r"user-data-dir={}".format(profile))

        # Instancia o Webdriver com o chromedriverManager que instala automaticamente o chromeDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Abre o Whatsapp Web
        self.driver.get('https://web.whatsapp.com')

        # Construtor da mensagem recebendo como parâmetro
        self.mensagem = mensagem

        # Aguarda 20 Segundos o site carregar
        time.sleep(20)

    # Abre mensgem para um contato mesmo se ele não estiver na lista de contato
    def buscarContato(self, number):
        try:
            # Busca o elemento para buscar o contato
            contato = self.driver.find_element("xpath", f"//*[@id='app']/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span")

            # Aguarda 3 Segundos para o elemento ser encontrado com sucesso
            time.sleep(3)

            # Clica no elemento contato
            contato.click()

            # Aguarda 3 Segundos para o elemento ser encontrado com sucesso
            time.sleep(3)

            # Busca a caixa de contato
            caixaContato = self.driver.find_element(By.XPATH, "//p[contains(@class, 'selectable-text copyable-text')]")

            # Aguarda 3 Segundos para o elemento ser encontrado com sucesso
            time.sleep(3)

            # Envia o numero de celular para ser buscado
            caixaContato.send_keys(number)

            # Aguarda 3 Segundos para o elemento ser encontrado com sucesso
            time.sleep(3)

            # Envia a tecla enter
            caixaContato.send_keys(Keys.ENTER)

            # Implementação para retornar True se conseguir encontrar o contato
            return True
        except:
            # Retorna False se não conseguir encontrar o contato
            return False


    def enviarMensagem(self):
        caixaMensagem = self.driver.find_elements(By.XPATH, "//p[contains(@class, 'selectable-text copyable-text')]")
        time.sleep(3)

        caixaMensagem[-1].send_keys(self.mensagem)
        botaoEnviar = self.driver.find_element(By.XPATH, "//span[@data-icon='send']")
        time.sleep(2)

        botaoEnviar.click()

    def enviarImagem(self, imagemPath):
        btnImg = self.driver.find_element(By.XPATH, "//span[@data-icon='attach-menu-plus']")
        time.sleep(3)

        btnImg.click()
        time.sleep(3)

        image_box = self.driver.find_element(By.XPATH,'//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        time.sleep(3)

        image_box.send_keys(imagemPath)
        time.sleep(3)

        caixaMensagem = self.driver.find_elements(By.XPATH, "//p[contains(@class, 'selectable-text copyable-text')]")
        caixaMensagem[0].send_keys(Keys.ENTER)

    def fecharMsg(self):
        btnMenu = self.driver.find_elements(By.XPATH, "//span[@data-icon='menu']")
        time.sleep(3)
        btnMenu[1].click()

        time.sleep(3)

        self.driver.find_element(By.XPATH, "//div[@aria-label='Fechar conversa']").click()