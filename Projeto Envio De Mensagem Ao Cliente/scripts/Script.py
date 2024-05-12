class projeto_envio():
    
    def __init__(self):
        self.data()
        self.leitura_base()
        self.transform_data()
        self.informacoes_clientes()
        self.envio_email()


    def data(self):   
        import datetime
        data = datetime.datetime.now()
        self.hoje = data.date()
        print(f'Data: {self.hoje}')
        
    def leitura_base(self):    
        #Importação Biblioteca
        import pandas as pd
        
        #Path/Caminho do arquivo
        path_arquivo = '../database/teste_envio.csv'
        
        #Leitura do arquivo .csv
        def leitura_arquivo(path, separador=';', idioma='latin-1'):
            
            arquivo = pd.read_csv(path, sep=separador,encoding=idioma)
            return arquivo
        #Arquivo "Lido"
        self.arquivo = leitura_arquivo(path=path_arquivo, idioma='latin-1')
         
    def transform_data(self):       
        #Tranformando a coluna "Telefone" no formato (00) 0000-0000,  Digamos que todos os DDD fossem iguais a 24, mas pode inserir outro valor na variavel DDD, que funcionara da mesma maneira
        def transformar_numero(dataframe,DDD='', coluna_a_transformar=''):
            dataframe[coluna_a_transformar] = f'({DDD})' + dataframe[coluna_a_transformar].astype(str)
            dataframe[coluna_a_transformar] = dataframe[coluna_a_transformar].apply(lambda x: f'{x[:9]}-{x[9:]}')
            return dataframe
        
        #Transformando a coluna "Data da Última Compra" em datetime
        def transformar_data(dataframe, formato='%d/%m/%Y', coluna_a_transformar=''):
            from pandas import to_datetime
            dataframe[coluna_a_transformar] = to_datetime(dataframe[coluna_a_transformar], format=formato)  
            return
            
        arquivo_transformado = self.arquivo.copy()
        transformar_numero(dataframe=arquivo_transformado, DDD=24, coluna_a_transformar='Telefone')
        transformar_data(dataframe=arquivo_transformado,coluna_a_transformar='Data da Última Compra')
        
        self.arquivo_transformado = arquivo_transformado.copy()
        
    def informacoes_clientes(self):
        #Extraindo dados dos clientes
        def coleta_dados_cliente(arquive=''):
            
            #Dicionário Vázio
            dic_dados_clientes = {}
            
            #Estrutura De Repetição
            for coluna, linha in arquive.iterrows():
                chave = coluna
                valor = linha.tolist()
                dic_dados_clientes[chave] = valor
            return dic_dados_clientes
        
        self.dados_clientes = coleta_dados_cliente(arquive=self.arquivo_transformado)     
        print(self.dados_clientes)
           
    def envio_email(self):
        print(f'Processo de Envio de E-mail Iniciado')
        #Dados Pessoais Para o Envio do e-mail
        import dados_pessoais
        #Bibliotecas E-mail
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        print(f'Bibliotecas importadas')
        
        #Salvando DF
        dados_clientes = self.dados_clientes
        
        indice_dados = {
            'ID':0,
            'NOME':1,
            'PGTO':2,
            'EMAIL':3,
            'TELEFONE':4,
            'ULT_COMPRA':5,
            'END':6
        }
        
        i = 0
        while i < len(dados_clientes):
            emails_info = {
                'host':'smtp.gmail.com',
                'port':'587',
                'login_email':dados_pessoais.email,
                'login_senha':dados_pessoais.senha,
                'destinatario':f'{dados_clientes[i][indice_dados['EMAIL']]}',
                'msg': f"""
Olá {dados_clientes[i][indice_dados['NOME']]}

Espero que esteja bem. Gostaríamos de agradecer pela sua última compra conosco em {dados_clientes[i][indice_dados['ULT_COMPRA']]}. Valorizamos muito a sua preferência!
Para facilitar sua experiência conosco, gostaríamos de confirmar suas informações de contato:

Forma de Pagamento: {dados_clientes[i][indice_dados['PGTO']]}
Email: {dados_clientes[i][indice_dados['EMAIL']]}
Telefone: {dados_clientes[i][indice_dados['TELEFONE']]}
Endereço: {dados_clientes[i][indice_dados['END']]}
Se alguma dessas informações mudou ou se há algo mais que gostaria de nos informar, por favor, nos avise. Estamos aqui para ajudar!

Atenciosamente,
E-mail Feito para portifólio, isso é apenas um Teste, Ignore Este E-mail Por Favor !! 
                """

            }
            
            server = smtplib.SMTP(emails_info['host'], emails_info['port'])
            server.ehlo()
            server.starttls()
            server.login(user=emails_info['login_email'], password=emails_info['login_senha'])
            
            email_msg = MIMEMultipart()
            email_msg['From'] = emails_info['login_email']
            email_msg['To'] = dados_clientes[i][indice_dados['EMAIL']]
            email_msg['Subject'] = 'Email Projeto Portifólio'
            email_msg.attach(MIMEText(emails_info['msg'], 'plain'))
            server.sendmail(email_msg['From'], emails_info['destinatario'], email_msg.as_string())
            server.quit()
            print(f'E-mail Enviado a: {emails_info["destinatario"]}, com a mensagem: {emails_info["msg"]}')
            i = i + 1