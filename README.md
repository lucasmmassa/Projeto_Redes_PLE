# Projeto de implementação de aplicação usando sockets para a disciplina de Redes de Computadores

## Grupo de projeto

* **Lucas Mendes Massa** - e-mail: lmm@ic.ufal.br - GitHub: https://github.com/lucasmmassa

* **Luana Júlia Nunes Ferreira** - e-mail: ljnf@ic.ufal.br - GitHub: https://github.com/ferreiraluana

## Descrição

O projeto implementado tem como intenção praticar o uso de sockets para a construção de um protocolo de aplicação em uma arquitetura cliente-servidor. Tendo isso em vista, foi implementada uma aplicação cuja funcionalidade é transformar textos recebidos através de uma requisição em vetores, fazendo uso de algoritmos de Processamento de Linguagem Natural (PLN), e devolver essas representações vetoriais como resposta para o cliente.

No que concerne aos algoritmos de PLN disponíveis para o usuário, ambos são bastante conhecidos na área. Mais informações a seu respeito podem ser encontradas nos links abaixo:

- Count Vectorizer: https://towardsdatascience.com/natural-language-processing-count-vectorization-with-scikit-learn-e7804269bb5e

- TF/IDF: https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089

Já no que concerne ao protocolo criado, o mesmo segue um padrão similar ao HTTP, contendo em sua primeira linha o comando enviado ao servidor e nas linhas subsequentes os textos a serem vetorizados. Caso a funcionalidade não exija nenhum texto para ser vetorizado, a mensagem contém apenas o comando. A mensagem se encerra com uma linha vazia.

````
FORMATO DA MENSAGEM ENVIADA QUANDO CONTÉM TEXTOS:

    COMANDO
    TEXTO 1
    TEXTO 2
    TEXTO 3
    ...
    TEXTO N
    LINHA VAZIA

FORMATO DA MENSAGEM ENVIADA QUANDO NÃO CONTÉM TEXTOS:

    COMANDO
    LINHA VAZIA
````

As respostas recebidas a partir das requisições seguem padrão similar. A primeira linha contém o status da requisição, indicando se a mesma foi bem sucedida ou não. Nas linhas subsequentes estarão contidas as coordenadas obtidas na vetorização dos textos, sendo coordenada separa por um caractere ; (ponto e vírgula). Caso a resposta não contenha coordenadas, a mesma se resume ao status da requisição. A resposta se encerra com uma linha vazia. Considerando um conjunto de n textos com representações vetoriais de m coordenadas, teríamos o seguinte formato:

````
FORMATO DA RESPOSTA CONTENDO VETORES:

    STATUS
    X11;X12;...;X1m
    X21;X22;...;X2m
    X31;X32;...;X3m
    ...
    Xn1;Xn2;...;Xnm
    LINHA VAZIA

FORMATO DA RESPOSTA SEM VETORES:

    STATUS
    LINHA VAZIA
````

As requisições podem resultar nos seguites códigos de status:

* 200 - SUCCESS: indica que uma requisição de vetorização foi bem sucedida;
* 300 - INVALID DATA: os textos dados de entrada não seguem o padrão exigido;
* 301 - ALGORITHM RUN FAILED: houve uma falha ao tentar executar o algoritmo nos textos enviados;
* 400 - INVALID COMMAND: o comando requisitado não faz parte da lista de comandos disponíveis;
* 500 DISCONNECTED: indica que a requisição de desconexão foi bem sucedida.

## Requisitos e instalação

Para que seja possível rodar o presente projeto em um computador é necessário que o mesmo tenha instaldo o sistema de controle de versão Git e a linguagem de programação Python 3. Além disso, deve-se seguir as instruções dadas nas subseções abaixo.

### Clonar o repositório

A fim de obter o código da aplicação pode-se baixar o códdigo zipado através do botão code na barra superior desta página ou clonar o repositório. Para clonar basta abrir o terminal, ir até o diretório onde se deseja salvar o repositório e digitar:

```
git clone https://github.com/lucasmmassa/Projeto_Redes_PLE.git
```

### Bibliotecas necessárias

Para executar o código do projeto é necessário intalar algumas bibliotecas que não vêm por padrão no Python 3, sendo elas numpy, pandas e scikit-learn. Para instalá-las basta usar o genreciador de pacotes do python, executando o seguinte código no terminal enquanto dentro do diretório raiz do projeto:

```
pip install -r requirements.txt
```

ou, a depender da versão do pip utilizada,

```
pip3 install -r requirements.txt
```

## Funcionamento da aplicação

Nas subseções a seguir será explicado como fazer uso da aplicação. Prrmeiramente é explicado como colocar o servidor em funcionamento. Em seguida são dadas instruções de como usar o cliente para fazer requisições ao servidor.

__Vale salientar que, para o correto funcionamento de uma aplicação cliente-servidor, o servidor deve ser colocado em funcionamento antes do cliente.__

### Servidor

Para colocar o servidor em funcionamento basta abrir o terminal na pasta raiz do projeto, navegar para dentro da pasta server e em seguida digitar o seguinte comando:

```
python server.py
```

![Servidor em funcionamento](/readme_images/server.png)

O servidor criará um socket e passará a escutar a porta 20000 para possíveis requisições de clientes. Como o servidor implementado usa threads, o mesmo aceita conexões com diferentes clientes simultaneamente. Mensagens mostrando o funcionamento e o recebimento de requisições são impressas no terminal.

### Cliente

Para fazer uso do cliente basta abrir o terminal na pasta raiz do projeto, navegar para dentro da pasta client e em seguida digitar o seguinte comando:

```
python client.py
``` 

Em seguida o programa pedirá ao usuário para digitar o endereço IP do servidor. Para se conectar a um servidor que esteja rodando na mesma máquina basta digitar "localhost". Caso o servidor esteja em uma máquina separada deve-se digitar o endereço IP da mesma.

![Cliente em funcionamento](/readme_images/client.png)

Assim que entrar em funcionamento, a aplicação solicitará do usuário um comando. O usuário deve digitar exatamente como é mostrado na lista dos comandos disponíveis, caso contrário obterá um erro de comando inválido. Os três comandos disponíveis são:

* "CV" : esse comando serve para o usuário enviar um conjunto de textos para o servidor e receber como resposta as representações vetoriais dos mesmos obtidas através do algoritmo Count Vectorizer.

* "TFIDF" : esse comando serve para o usuário enviar um conjunto de textos para o servidor e receber como resposta as representações vetoriais dos mesmos obtidas através do algoritmo TF/IDF.

* "DISCONNECT" : esse comando serve para o usuário encerrar a conexão com o servidor e finalizar a execução do cliente.

Os dois primeiros comandos da lista irão exigir que o usuário informe o caminho para um arquivo contendo os textos a serem enviados ao servidor através do protocolo criado. __Esse arquivo deve seguir algumas restrições__:

* deve ser um arquivo em formato csv;
* a coluna contendo os textos deve se chamar "content";
* a coluna de textos não pode conter elementos vazios nem ser completamente vazia, tendo em vista que impactaria na formatação da mensagem de requisição e na execução do algoritmo de PLN por parte do servidor;
* o arquivo deve ter no máximo 40MB;
* os textos devem ter codificação UTF-8.

Para fins de teste foi disponibilizado um arquivo no formato exigido dentro da pasta client. O arquivo se chama bbc.csv e contém conteúdo extraído de algumas matérias das págins web da BBC em português.

#### Comando CV

Ao digitar esse comando, o programa exigirá do usuário o caminho para um arquivo de entrada. Caso o arquivo siga as restrições explicadas, o seu conteúdo será formatado e uma requisição será feita ao servidor.

![Comando CV](/readme_images/cv.png)

Caso a requisição seja bem sucedida, uma mensagem contendo STATUS 200 será exibida. Além disso, para fins de teste, um arquivo test.npy será criado contendo o resultado da vetorização dos textos em formato de numpy array.

#### Comando TFIDF

Ao digitar esse comando, o programa exigirá do usuário o caminho para um arquivo de entrada. Caso o arquivo siga as restrições explicadas, o seu conteúdo será formatado e uma requisição será feita ao servidor.

![Comando CV](/readme_images/tfidf.png)

Caso a requisição seja bem sucedida, uma mensagem contendo STATUS 200 será exibida. Além disso, para fins de teste, um arquivo test.npy será criado contendo o resultado da vetorização dos textos em formato de numpy array.

#### Comando DISCONNECT

Ao digitar esse comando, o programa não exigirá mais nenhuma ação do usuário, enviando uma requisição para o servidor contendo apenas o comando.

![Comando CV](/readme_images/disconnect.png)

Caso a requisição seja bem sucedida, uma mensagem contendo STATUS 500 será exibida e o programa cliente será encerrado.