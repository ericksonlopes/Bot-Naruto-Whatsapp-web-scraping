from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


def pesquisa_web(pesquisa):
    pagina = requests.get('https://naruto.fandom.com/pt-br/wiki/' + pesquisa.lower())
    if pagina.status_code == 200:
        print('sucesso ao encontrar a página')
        soup = BeautifulSoup(pagina.content, 'html.parser')

        nome_personagem = soup.find(class_="page-header__title").get_text()
        lista = []
        for item in soup.find_all('p'):
            personagem = item.get_text()
            lista.append(personagem.strip('\n'))
        else:
            resumo = []
            for item in lista:
                if nome_personagem in item:
                    resumo.append(item)
                    break
            return resumo[0]
    else:
        return 'erro ao encontrar a página', pesquisa


class PesquisaNinja:
    def __init__(self):

        try:
            # instância o local do cromedriver
            self.chrome = webdriver.Chrome()
            # Recebe o site que precisa entrar
            self.chrome.get('https://web.whatsapp.com/')
            time.sleep(10)
        except Exception as err:
            print('Erro: chromedriver | acesso ao site\n', err)
        else:
            lista = []
            while True:
                time.sleep(10)

                ultimas_conversas = self.chrome.find_elements_by_class_name('_2wP_Y')
                for item in ultimas_conversas:
                    lista.append(item.text)

                for itens in lista:
                    lista_itens = itens.split('\n')
                    for item in lista_itens:
                        if '/ninja' in item:
                            print(lista_itens)
                            nome = lista_itens[0]
                            pesquisa = item.split('/ninja')[1:]
                            print(nome, 'Pesquisou', pesquisa[0])
                            self.pesquisar_ninja(nome, pesquisa[0])

                time.sleep(20)
                self.chrome.refresh()
                ultimas_conversas.clear()
                lista.clear()

    def pesquisar_ninja(self, contato, pesquisa):
        try:
            caixa_contato = self.chrome.find_element_by_xpath(f'//span[@title="{contato}"]')
            caixa_contato.click()
            self.enviar_mensagem(contato, 'Sua pesquisa está sendo feita!')

            mensagem = pesquisa_web(pesquisa)
            print(mensagem)
        except Exception as err:
            print('Não foi possível pesquisar: {contato} -> {mensagem}\n', err, '\n')
            self.enviar_mensagem(contato, f'Desculpe! não encontrei palavra-chave para sua pesquisa')
        else:
            self.enviar_mensagem(contato, mensagem)
            self.enviar_mensagem(contato, f'Você pesquisou sobre: {pesquisa}')

    def receber_mensagem_contato(self, contato):
        try:
            caixa_contato = self.chrome.find_element_by_xpath(f'//span[@title="{contato}"]')
            caixa_contato.click()
            post = self.chrome.find_elements_by_class_name("_3_7SH")
            ultimo = len(post) - 1
            # O texto da ultima mensagem
            texto_recebido = post[ultimo].find_element_by_css_selector("span.selectable-text").text
        except Exception as err:
            print('Não foi possível enviar a mensagem\n', err)
        else:
            return texto_recebido

    def enviar_mensagem(self, contato, mensagem):
        try:
            primeira_caixa = self.chrome.find_element_by_xpath(f'//span[@title="{contato}"]')
            primeira_caixa.click()
            caixa_texto = self.chrome.find_element_by_class_name('_1Plpp')
            caixa_texto.send_keys(mensagem)
            time.sleep(0.30)
            btn_enviar = self.chrome.find_element_by_xpath('//span[@data-icon="send"]')
            btn_enviar.click()
        except Exception as err:
            print('Erro ao enviar mensagem\n', err)


if __name__ == '__main__':
    PesquisaNinja()
