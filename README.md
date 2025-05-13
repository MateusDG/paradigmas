## **Comparação de Paradigmas - Imperativo vs. Orientado a Objetos com Abstração**

**Objetivo:** Compreender como os paradigmas imperativo e orientado a objetos abordam a solução de problemas de maneira diferente, explorando conceitos como controle de fluxo, encapsulamento e abstração.

**Enunciado:**

Você foi contratado para desenvolver uma aplicação simples para um sistema de **streaming de música** . Esse sistema deve permitir que os usuários escutem músicas, adicionem músicas a playlists e exibam informações de cada faixa.

A aplicação precisa implementar as seguintes operações:

1. **Reproduzir uma música** : ao escolher uma música, o sistema inicia a reprodução e exibe informações básicas, como título, artista e duração.
2. **Adicionar música a uma playlist** : permite que o usuário crie playlists e adicione músicas a elas.
3. **Mostrar informações da playlist** : exibe o nome da playlist e a lista de músicas nela contida.
4. **Listar todas as músicas disponíveis** no catálogo.

## **Instruções:**

### * **Identificação de Abstrações** :

* Identifique as abstrações naturais deste problema e explique por que “Música”, “Playlist” e “Catálogo” são boas escolhas para abstrações.
* Descreva como essas abstrações ajudam a ocultar detalhes específicos (como a reprodução de áudio ou a manipulação de listas) e simplificam o desenvolvimento do sistema.

### * **Implementação Imperativa** :

* Descreva como resolveria esse problema usando o paradigma imperativo, sem abstrações significativas.
* **Crie um código imperativo que:**
  * Use variáveis para representar a lista de músicas, playlists, e informações de cada música.
  * Utilize estruturas de controle (como if e while) para gerenciar a adição de músicas a playlists e a reprodução de músicas.
  * Manipule diretamente as variáveis para exibir informações de músicas e playlists.
* **Reflexão sobre Abstração:** Explique como a abordagem imperativa lida com abstração e quais limitações você observa se o sistema for ampliado para incluir novos recursos, como busca avançada por artistas ou gêneros.

### * **Implementação Orientada a Objetos** :

* Descreva como resolveria o problema usando o paradigma orientado a objetos, aproveitando a abstração.
* **Crie um código orientado a objetos que:**
  * Inclua uma classe Musica com atributos como titulo, artista, duracao.
  * Crie uma classe Playlist que contém uma lista de objetos Musica e métodos para adicionar músicas e exibir a lista de músicas.
  * Crie uma classe Catalogo que contém a lista completa de músicas disponíveis e fornece métodos para buscar e listar músicas.
  * Utilize encapsulamento para que detalhes como listas e métodos de manipulação sejam ocultados do usuário final.
* **Reflexão sobre Abstração**: Explique como a abstração no paradigma orientado a objetos ajuda a modularizar o código e a tornar o sistema mais flexível para adições de novas funcionalidades, como recomendações ou filtros.

### * **Comparação e Discussão** :

* **Compare as duas implementações e responda às perguntas a seguir:**
  * Qual implementação é mais fácil de modificar, caso um novo recurso (como filtro por gênero) precise ser adicionado?
  * Qual abordagem permite um controle mais seguro e abstrato das músicas e playlists? Justifique.
  * Em qual caso o fluxo do programa ficou mais fácil de entender?
  * Discuta como o conceito de abstração é tratado em cada paradigma, focando nas vantagens de organizar e ocultar detalhes em um sistema que pode crescer em complexidade.
