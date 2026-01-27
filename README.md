# Provas da Peroba 📚

Uma aplicação web interativa de quiz desenvolvida com Streamlit para testar e consolidar conhecimentos em diversas matérias.

## 🎯 Funcionalidades

- **Quiz por Matéria**: Teste seus conhecimentos com questões organizadas por matéria
- **Feedback Imediato**: Saiba na hora se acertou ou errou cada questão
- **Progresso em Tempo Real**: Acompanhe seu progresso com barra de progresso e contadores
- **Estudo Customizado**: Carregue seus próprios arquivos CSV para estudar
- **Interface Amigável**: Design responsivo e intuitivo com navegação simplificada
- **Resultados Detalhados**: Visualize seu desempenho ao final de cada quiz

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install streamlit pandas
```

3. Execute a aplicação:

```bash
streamlit run nome_do_arquivo.py
```

4. Acesse no navegador: `http://localhost:8501`

## 📁 Estrutura do Projeto

```
provas_da_peroba/
├── app.py                    # Código principal da aplicação
├── questoes/                 # Pasta para arquivos CSV das questões
│   ├── matematica.csv
│   ├── portugues.csv
│   └── outras_materias.csv
└── README.md
```

## 📝 Formato dos Arquivos de Questões

Os arquivos CSV devem seguir este formato (sem cabeçalho):

```
"Pergunta completa?","Opção A","Opção B","Opção C","Opção D","a"
"Outra pergunta?","Resposta A","Resposta B","Resposta C","Resposta D","c"
```

**Importante:**
- O arquivo NÃO deve ter cabeçalho
- 6 colunas: pergunta, opção A, opção B, opção C, opção D, resposta correta
- A resposta correta deve ser 'a', 'b', 'c' ou 'd'
- Use aspas para envolver textos com vírgulas

## 🎮 Como Usar

### 1. Modo Quiz Padrão
- Acesse a seção "📝 Quiz" no menu lateral
- Selecione uma matéria da lista (arquivos CSV da pasta `questoes/`)
- Clique em "▶️ Iniciar Quiz"
- Responda as questões clicando nas opções
- Navegue entre questões com os botões "Anterior" e "Próxima"
- Veja seus resultados ao final

### 2. Modo Estudo Customizado
- Acesse "🔧 Estudo Customizado" no menu
- Faça upload do seu próprio arquivo CSV
- Siga o mesmo formato descrito acima
- Clique em "▶️ Iniciar Quiz Personalizado"

### 3. Página Inicial
- Contém informações sobre o aplicativo
- Explica como usar cada funcionalidade
- Fornece contato para sugestões

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web em Python
- **Pandas**: Manipulação e análise de dados
- **Python 3**: Linguagem de programação principal

## 🎨 Personalização

### Adicionar Novas Questões
1. Crie um arquivo CSV no formato especificado
2. Salve na pasta `questoes/`
3. O arquivo aparecerá automaticamente no seletor de matérias

### Modificar o Estilo
O CSS customizado está no início do código. Você pode alterar:
- Cores (`#2E86AB`, `#A23B72`, etc.)
- Estilos dos cards
- Cores de feedback (acertos/erros)

## ⚠️ Solução de Problemas

### Problema: "Nenhum arquivo CSV encontrado"
**Solução:** Crie a pasta `questoes/` no mesmo diretório do arquivo Python

### Problema: Erro ao carregar arquivo CSV
**Solução:** Verifique se o arquivo segue exatamente o formato especificado

### Problema: Botões não respondem
**Solução:** Recarregue a página (F5) ou clique em "🔄 Reiniciar"

## 👥 Autor

**João da Petrobras**  
[GitHub](https://github.com/joao-petro)  
Contato via Teams (GFGQ)

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de estudo.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Entre em contato via Teams.

---

*Criado com ❤️ para auxiliar nos estudos e na preparação para provas*